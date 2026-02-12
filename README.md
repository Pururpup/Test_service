# Мини-сервис управления заказами
Этот проект представляет собой REST API для системы управления заказами.

Данный сервис позволяет:
- создавать клиентов и заказы;
- добавлять товары в заказ;
- считать сумму заказа;
- фильтровать заказы по статусу, дате и клиенту.


## Оглавление
- Стек технологий 
- Установка
  - Требования
- Запуск
- Переменные окружения
- Доступ к сервису
- Структура проекта
- Примеры использования API
- Работа с Celery


## Стек технологий
- Python 3.x
- Django
- Django REST Framework
- PostgreSQL
- Docker
- Docker Compose


## Установка

### Требования
- Docker
- Docker Compose

Клонируйте репозиторий:
```bash
git clone https://github.com/Pururpup/Test_service
cd OrderService
```


## Запуск
Запуск проекта осуществляется с помощью Docker:
```bash
docker compose up --build -d
```

После запуска примените миграции:
```bash
docker compose exec web python manage.py migrate
```

(Опционально) создайте суперпользователя для доступа к админ-панели:
```bash
docker compose exec web python manage.py createsuperuser
```


## Переменные окружения
В корне проекта необходимо создать файл .env:
```dotenv
POSTGRES_DB=service_db
POSTGRES_USER=service_user
POSTGRES_PASSWORD=service_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

CELERY_BROKER_URL="redis://redis:6379/0"
CELERY_RESULT_BACKEND="django-db"
```


## Доступ к сервису
- API: http://localhost:8000/
- Admin: http://localhost:8000/admin/


## Структура проекта
```markdown
OrderService/
├── backend/
│   ├── config/
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── celery.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py 
│   ├── service_app/
│   │   ├── migrations/
│   │   │   └── __init__.py
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── test_customer_api.py
│   │   │   ├── test_order_api.py
│   │   │   └── test_product_api.py
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tasks.py
│   │   └── views.py
│   ├── __init__.py
│   └── manage.py
├── .env
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── poetry.lock
├── pyproject.toml
└── README.md
```


## Примеры использования API
Получить список клиентов:
```bash
curl -X GET http://localhost:8000/api/customers/
```

Создать клиента:
```bash
curl -X POST http://localhost:8000/api/customers/ \
-H "Content-Type: application/json" \
-d '{"name": "Иван Иванов", "email": "ivan@example.com"}'
```

Получить список товаров:
```bash
curl -X GET http://localhost:8000/api/products/
```

Создать товар:
```bash
curl -X POST http://localhost:8000/api/products/ \
-H "Content-Type: application/json" \
-d '{"name": "Ноутбук", "price": 50000, "stock": 10}'
```

Получить список заказов с фильтрацией:
```bash
# Все заказы
curl -X GET http://localhost:8000/api/orders/

# Фильтр по статусу
curl -X GET "http://localhost:8000/api/orders/?status=paid"

# Фильтр по клиенту
curl -X GET "http://localhost:8000/api/orders/?customer_id=1"

# Фильтр по дате создания (YYYY-MM-DD)
curl -X GET "http://localhost:8000/api/orders/?created_at=2026-01-18"
```

Создать заказ:
```bash
curl -X POST http://localhost:8000/api/orders/ \
-H "Content-Type: application/json" \
-d '{"customer_id": 1, "status": "new"}'
```

Получить детали конкретного заказа:
```bash
curl -X GET http://localhost:8000/api/orders/1/
```

Изменить статус заказа:
```bash
curl -X PATCH http://localhost:8000/api/orders/1/status/ \
-H "Content-Type: application/json" \
-d '{"status": "paid"}'
```

Добавить товар в заказ:
```bash
curl -X POST http://localhost:8000/api/orders/1/items/ \
-H "Content-Type: application/json" \
-d '{"product_id": 2, "quantity": 3}'
```


## Работа с Celery
В проекте реализована фоновая задача Celery, которая автоматически удаляет отмененные заказы из базы данных.
Задача очищает базу данных от заказов со статусом "cancelled".

Запуск:
Celery worker и Celery Beat запускаются как отдельные сервисы в docker-compose.yml и поднимаются автоматически вместе с проектом.

