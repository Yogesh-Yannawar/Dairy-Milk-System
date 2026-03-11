from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment_list, name='payment_list'),
    path('generate/', views.generate_bill, name='generate_bill'),
    path('<int:pk>/', views.payment_detail, name='payment_detail'),
    path('<int:pk>/mark-paid/', views.mark_paid, name='mark_paid'),
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/add/', views.customer_add, name='customer_add'),
]
