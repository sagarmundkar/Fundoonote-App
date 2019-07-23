import self
from celery import shared_task
from celery.utils.log import get_task_logger


from .mail import Mailer
from .models import Note, Label

import datetime
import mysql.connector
from celery import Celery
from celery.schedules import crontab

logger = get_task_logger(__name__)


@shared_task
def update_notes(notes_id, title):  # rename the title
    note = Note.objects.get(id=notes_id)
    note.title = title  # take title field
    note.save()
    return note


@shared_task
def update_label(label_id, text):  # update label
    label = Label.objects.get(id=label_id)
    label.text = text
    label.save()


@shared_task(name="send_email_task")
def send_feedback_email_task(name, email, message):
    logger.info("Sent email")
    return send_feedback_email_task(name, email, message)


app = Celery('Fundoonotes', broker="amqp://localhost")
# disable UTC so that Celery can use local time
app.conf.enable_utc = False


@app.task
def noteapp_notes_today():
    conn = mysql.connector.connect(
        user='root', database='notes', password='Admin@123')
    curs = conn.cursor()
    today = datetime.datetime.now()
    query = """SELECT title, id FROM notes
    WHERE month(reminder_date)={0} and day(reminder_date)={1};""".format(
        today.month, today.day)
    curs.execute(query)
    for (title, id) in curs:
        print(
            """
            Hi {0} {1},
           
            """.format(title, id)
        )
    curs.close()
    conn.close()


# add "birthdays_today" task to the beat schedule
app.conf.beat_schedule = {
    "note-task": {
        "task": "Fundoonotes.noteapp_notes_today",
        "schedule": crontab(hour=1, minute=0)
    }
}

mail = Mailer()
mail.send_messages(subject='Email verification',
                   template='noteapp/welcom.html',
                   context={'user': self},
                   to_emails=['shreemundkar@gmail.com', 'admin@gmail.com'])
