"""
URL configuration for service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from service_app.views import OrderAPIView, OrderDetailAPIView, \
    OrderStatusAPIView, OrderItemsAPIView, ProductViewSet, CustomerViewSet, get_order_statistics

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'customers', CustomerViewSet, basename='customers')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/orders/<int:pk>/status/', OrderStatusAPIView.as_view(), name='orders-status'),
    path('api/orders/<int:pk>/items/', OrderItemsAPIView.as_view(), name='orders-item'),
    path('api/orders/<int:pk>/', OrderDetailAPIView.as_view()),
    path('api/orders/', OrderAPIView.as_view(), name='orders-list'),

    path('api/', include(router.urls)),

    path('order-statistics/', get_order_statistics)

]