from datetime import timedelta
from celery import shared_task
from django.utils import timezone
from django.core.files.base import ContentFile
from django.db.models import Sum, F
from io import BytesIO

from minio_storage import MinioMediaStorage

from service_app.models import Order, OrderItem
from openpyxl import Workbook

# Celery-задача: раз в минуту отменять старые неоплаченные заказы (`status → cancelled`)
@shared_task
def delete_cancelled_orders():
    Order.objects.filter(status='cancelled').delete()

# Celery-задача: раз в час (либо по запросу) брать все заказы за месяц и считать их сумму
@shared_task
def order_statistics():
    month_ago = timezone.now() - timedelta(days=30)
    order_sum = (
        OrderItem.objects
        .filter(order__created_at__gte=month_ago)
        .values('order_id')
        .annotate(total_price=Sum(F("quantity") * F("price_at_order")))
    ) # сумма по каждому заказу

    total_quantity = order_sum.count() # общее количество заказов
    total_sum = order_sum.aggregate(total_sum=Sum('total_price'))['total_sum'] or 0 # общая сумма по всем заказам

    wb = Workbook() # создали новую книгу
    sheet = wb.active # создали активный лист
    sheet.title = "Orders"

    sheet.append(['ID заказа', 'Итоговая сумма заказа', 'Общее количество заказов', 'Итоговая сумма всех заказов'])

    for item in order_sum:
        sheet.append([item['order_id'], item['total_price'], '', ''])

    sheet.append(['', '', total_quantity, total_sum])

    # сохраняем файл в память
    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    # сохраняем файл в minio
    storage = MinioMediaStorage()
    file_name = 'order_statistics.xlsx'

    if storage.exists(file_name):
        storage.delete(file_name)

    storage.save(file_name, ContentFile(buffer.read()))



