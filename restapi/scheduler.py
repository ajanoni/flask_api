import uuid
import queue
from datetime import datetime
from threading import RLock

from apscheduler.schedulers.background import BackgroundScheduler

from restapi.content import Content

scheduled_jobs = {}  # We could use a queue Redis or Kafka in replacement here and persistence
DATETIME_FORMAT = "%Y-%m-%d %H:%M"
lock = RLock()


def schedule_content(scheduled_datetime, new_content):
    content = Content(str(uuid.uuid4()), new_content)
    scheduled_jobs.setdefault(scheduled_datetime.strftime(DATETIME_FORMAT), queue.Queue()).put(content)
    return content.id


# In order to scale, this part should be deployed as separated worker instances consuming from a queue
def print_values():
    date_queue = scheduled_jobs.get(datetime.now().strftime(DATETIME_FORMAT))
    if date_queue:
        while not date_queue.empty():
            content_item = date_queue.get()
            print(content_item.content)


scheduler_background = BackgroundScheduler()
job = scheduler_background.add_job(print_values, 'interval', seconds=1)
scheduler_background.start()
