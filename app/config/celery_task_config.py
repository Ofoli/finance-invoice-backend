from celery.schedules import crontab

timezone = "UTC"
accept_content = ["json", "msgpack", "yaml"]
task_serializer = "json"
result_serializer = "json"
worker_max_tasks_per_child = 20

beat_schedule = {
    "test-celery": {
        "task": "app.core.report.tasks.test_celery",
        "schedule": crontab(minute="*"),
    },
    "initiate-s3-report-script": {
        "task": "app.core.report.tasks.initiate_s3_fetch_script",
        "schedule": crontab(minute="*/2")
    }
}
