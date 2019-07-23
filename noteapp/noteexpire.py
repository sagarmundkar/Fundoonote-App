import datetime
import mysql.connector
from celery import Celery
from celery.schedules import crontab

app = Celery('Fundoonotes', broker="amqp://localhost")
# disable UTC so that Celery can use local time
app.conf.enable_utc = False


@app.task
def birthdays_today():
    conn = mysql.connector.connect(
        user='root', database='notes', password='')
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
            We would like to wish you a great birthday and a 
            memorable year.
            From all of us at company ABC.
            """.format(title, id)
        )
    curs.close()
    conn.close()


# add "birthdays_today" task to the beat schedule
app.conf.beat_schedule = {
    "birthday-task": {
        "task": "Fundoonotes.birthdays_today",
        "schedule": crontab(hour=1, minute=0)
    }
}
