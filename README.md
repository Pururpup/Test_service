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
cd Test_service
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
DEBUG=True
SECRET_KEY=your-secret-key

POSTGRES_DB=service_db
POSTGRES_USER=service_user
POSTGRES_PASSWORD=service_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
```


## Доступ к сервису
- API: http://localhost:8000/
- Admin: http://localhost:8000/admin/


## Структура проекта
Test_service/
├── service/
│   ├── service/    # настройки Django
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── service_app/    # основное приложение
│   │   ├── migrations/
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
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