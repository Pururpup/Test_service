import os
from datetime import timedelta
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('backend') # экземпляр Celery-приложения

# сконфигурировали приложение
app.config_from_object("django.conf:settings", namespace="CELERY")

# автоматический поиск tasks во всех приложениях из INSTALLED_APPS
# найденная задача будет импортирована и зарегистрирована в Celery
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "delete_cancelled_orders": {
        "task": "service_app.tasks.delete_cancelled_orders",
        "schedule": 60.0,
    },

    "order_statistics": {
        "task": "service_app.tasks.order_statistics",
        "schedule": timedelta(hours=1)
    },
}