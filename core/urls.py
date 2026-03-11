from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard_root'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('milk-rates/', views.milk_rates, name='milk_rates'),
    path('users/', views.user_management, name='user_management'),
]
