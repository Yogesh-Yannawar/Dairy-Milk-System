from django.urls import path
from . import views

urlpatterns = [
    path('daily/', views.daily_report, name='daily_report'),
    path('monthly/', views.monthly_report, name='monthly_report'),
    path('payments/', views.payment_report, name='payment_report'),
    path('fat/', views.fat_report, name='fat_report'),
]
