from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('history/', views.order_history_view, name='order_history'),
    path('<int:order_id>/', views.order_detail_view, name='order_detail'),
]