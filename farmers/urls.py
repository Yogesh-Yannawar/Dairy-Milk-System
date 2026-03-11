from django.urls import path
from . import views

urlpatterns = [
    path('', views.farmer_list, name='farmer_list'),
    path('add/', views.farmer_add, name='farmer_add'),
    path('<int:pk>/', views.farmer_detail, name='farmer_detail'),
    path('<int:pk>/edit/', views.farmer_edit, name='farmer_edit'),
    path('<int:pk>/delete/', views.farmer_delete, name='farmer_delete'),
]
