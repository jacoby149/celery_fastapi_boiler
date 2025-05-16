import subprocess
from watchgod import watch

def start_celery_worker():
    return subprocess.Popen(
        [
            "pipenv",
            "run",
            "celery",
            "-q",
            "-A",
            "celery_starter.celery_app",
            "worker",
            "--loglevel=info",
            ]    
    )

if __name__ == "__main__":
    process = start_celery_worker()
    print("Watching for file changes...")

    #Check for changes
    for changes in watch("./"):
        for change_type, path in changes:
            if path.endswith(".py"):
                print(f"Detected change in {path}, restarting Celery worker...")
                process.terminate()
                process.wait()
                process.start_celery_worker()
                # break because we only need to restart once.
                # i.e. if there are multiple events, just restart once.
                break
