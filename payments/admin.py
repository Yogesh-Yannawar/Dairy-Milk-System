from django.contrib import admin
from .models import Payment, Customer, CustomerPayment
admin.site.register(Payment)
admin.site.register(Customer)
admin.site.register(CustomerPayment)
