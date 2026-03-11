from django.contrib import admin
from .models import MilkCollection, Inventory, InventoryTransaction
admin.site.register(MilkCollection)
admin.site.register(Inventory)
admin.site.register(InventoryTransaction)
