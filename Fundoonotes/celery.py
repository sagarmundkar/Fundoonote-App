from __future__ import absolute_import, unicode_literals
from celery.schedules import crontab

import os
from celery import Celery

# Setting the Default Django settings module
from celery.utils.log import get_task_logger

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Fundoonotes.settings')
app = Celery('Fundoonotes',
             broker='amqp://localhost',
             backend='rpc://',
             include=['noteapp.tasks'])

# Using a String here means the worker will always find the configuration information
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.result_expires = 60

app.conf.beat_schedule = {
    'remove-notes-daily-at-midnight': {
        'task': 'noteapp.tasks.remove_notes',
        'schedule': crontab(minute=0, hour=0),
    },
}


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Sending the email every 10 Seconds
    sender.add_periodic_task(10.0, send_feedback_email_task.s('sagarmundkar', 'sagarmundkar13@gmail.com', 'Hello'),
                             name='add every 10')
    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        send_feedback_email_task.s('sagarmundkar', 'sagarmundkar13@gmail.com', 'Hello'), )


# The task to be processed by the worker
def send_feedback_email_task(name, email, message):
    pass


logger = get_task_logger(__name__)


@app.task
def send_feedback_email_task(name, email, message):
    send_feedback_email_task(name, email, message)
    logger.info("Sent email")
