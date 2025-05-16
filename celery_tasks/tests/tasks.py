import redis
from contextlib import contextmanager
from services.celery_test.test import wait_and_print_job_id
import settings
from celery_app import celery_app

# FIRST task without lock
@celery_app.task
def task_wait_and_print_job_id(job_id, wait_time):
    return wait_and_print_job_id(job_id, wait_time)

# Create a Redis client
redis_client = redis.Redis.from_url(settings.CELERY_BROKER_URL)

# Define a context manager for Redis locking
@contextmanager
def redis_lock(lock_name, timeout=60):
    """
    Acquires a Redis lock with a given name and timeout.
    Raises an Exception if the lock cannot be acquired.
    """
    lock = redis_client.lock(lock_name, timeout=timeout)
    acquired = lock.acquire(blocking=True)
    try:
        if acquired:
            yield lock
        else:
            raise Exception(f"Could not acquire lock: {lock_name}")
    finally:
        if acquired:
            lock.release()

# SECOND task that wraps the original function with a Redis lock
@celery_app.task
def task_with_redis_id_lock(job_id, wait_time):
    lock_key = f"lock:job_id:{job_id}"
    with redis_lock(lock_key, timeout=60):
        return wait_and_print_job_id(job_id, wait_time)
