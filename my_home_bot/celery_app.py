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
    'check-tasks-every-3-hours': {
        'task': 'tasks.check_tasks',
        'schedule': crontab(minute=0, hour='*/3'),  # Запускать каждые 3 часа
    },
    'mark-old-tasks-every-3-hours': {
        'task': 'tasks.old_tasks',
        'schedule': crontab(minute=0, hour='*/3'),  # Запускать каждые 3 часа
    },
}