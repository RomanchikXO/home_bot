from celery import Celery
from celery.schedules import crontab


app = Celery('tasks', broker='redis://localhost:6379/0')

app.conf.update(
    result_backend='redis://localhost:6379/0',
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='Europe/Moscow',
    enable_utc=True,
)

from tasks import check_tasks, old_tasks
app.conf.beat_schedule = {
    'check-tasks-every-day-at-midnight-one-minute': {
        'task': 'tasks.check_tasks',
        'schedule': crontab(hour=0, minute=20),  # Запускать check_tasks каждый день в 00:20
    },
    'mark-old-tasks-every-day-at-midnight-one-minute': {
        'task': 'tasks.old_tasks',
        'schedule': crontab(hour=0, minute=20),  # Запускать old_tasks каждый день в 00:20
    },
}