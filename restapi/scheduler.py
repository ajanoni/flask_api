from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

scheduledJobs = {}
DATETIME_FORMAT = "%Y-%m-%d %H:%M"


def schedule_content(scheduled_datetime, content):
    scheduledJobs.setdefault(scheduled_datetime.strftime(DATETIME_FORMAT), []).append(content)
    print_values()


def print_values():
    filtered = {key: value for (key, value) in scheduledJobs.items()
                if key == datetime.now().strftime(DATETIME_FORMAT)}
    for key, value in filtered.items():
        for content in value:
            print(content)
        scheduledJobs.pop(key)


scheduler_background = BackgroundScheduler()
job = scheduler_background.add_job(print_values, 'interval', seconds=3)
scheduler_background.start()
