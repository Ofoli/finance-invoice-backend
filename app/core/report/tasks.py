import celery


@celery.shared_task(ignore_result=False)
def test_celery() -> str:
    return "testing...."
