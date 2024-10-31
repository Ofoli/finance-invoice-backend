from celery.schedules import crontab

timezone = "UTC"
accept_content = ["json", "msgpack", "yaml"]
task_serializer = "json"
result_serializer = "json"
worker_max_tasks_per_child = 20

beat_schedule = {
    "initiate-s3-report-script": {
        "task": "app.core.report.tasks.initiate_s3_fetch_script",
        "schedule": crontab(minute="0", hour="1", day_of_month="1"),
    },
    "initiate-etz-report-script": {
        "task": "app.core.report.tasks.initiate_etz_report_script",
        "schedule": crontab(minute="0", hour="2", day_of_month="1"),
    },
}
