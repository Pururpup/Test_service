from celery import shared_task

from service_app.models import Order


# Celery-задача: раз в день отменять старые неоплаченные заказы (`status → cancelled`)
@shared_task
def delete_cancelled_orders():
    Order.objects.filter(status='cancelled').delete()
