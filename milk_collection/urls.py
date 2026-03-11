from django.urls import path
from . import views

urlpatterns = [
    path('', views.collection_list, name='collection_list'),
    path('add/', views.collection_add, name='collection_add'),
    path('<int:pk>/edit/', views.collection_edit, name='collection_edit'),
    path('<int:pk>/delete/', views.collection_delete, name='collection_delete'),
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/add/', views.inventory_add, name='inventory_add'),
    path('inventory/<int:pk>/stock/', views.stock_transaction, name='stock_transaction'),
]
