from fastapi import APIRouter, HTTPException, UploadFile, Form, File, Query
from pydantic import BaseModel
from typing import List, Optional
from services.celery_test.test import wait_and_print_job_id
from celery_tasks.tests.tasks import task_wait_and_print_job_id
from celery_tasks.tests.tasks import task_with_redis_id_lock

router = APIRouter()

class TestCeleryInput(BaseModel):
    submission_id: int
    wait_time: int

test_inputs = [
    TestCeleryInput(submission_id=1, wait_time=1),
    TestCeleryInput(submission_id=2, wait_time=1),
]

@router.post("/no_celery/bad")
async def no_celery(test_input: TestCeleryInput):
    """
    to test triggering a celery task with an api endpoint.
    this is how a webhook will do its thing!
    """
    for test_input in test_inputs:
        wait_and_print_job_id(test_input.model_dump())
    return "success all processed!"

@router.post("/simple_celery")
async def simple_celery():
    for test_input in test_inputs:
        task_wait_and_print_job_id.apply_async(kwargs=test_input.model_dump())
    return "success, pushed to queue!"

@router.post("/locking_celery")
async def locking_celery():
    for test_input in test_inputs:
        task_with_redis_id_lock.apply_async(kwargs=test_input.model_dump())
    return "success, pushed to queue!"
