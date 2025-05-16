"""
test function
"""
import time

def wait_and_print_job_id(job_id,wait_time):
    time.sleep(wait_time)
    print(f"job id {job_id} processed!")
