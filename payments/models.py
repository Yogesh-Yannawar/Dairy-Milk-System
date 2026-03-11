from django.db import models
from farmers.models import Farmer

class Payment(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('paid', 'Paid'), ('partial', 'Partial')]
    PERIOD_CHOICES = [('weekly', 'Weekly'), ('monthly', 'Monthly')]
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='payments')
    period_type = models.CharField(max_length=10, choices=PERIOD_CHOICES, default='monthly')
    from_date = models.DateField()
    to_date = models.DateField()
    total_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    payment_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.farmer.name} - {self.from_date} to {self.to_date}"

    @property
    def due_amount(self):
        return self.total_amount - self.paid_amount

    class Meta:
        ordering = ['-created_at']

class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    milk_per_day = models.DecimalField(max_digits=5, decimal_places=2, default=1)
    rate_per_liter = models.DecimalField(max_digits=6, decimal_places=2, default=50)
    joining_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class CustomerPayment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='payments')
    from_date = models.DateField()
    to_date = models.DateField()
    total_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} - {self.from_date}"
