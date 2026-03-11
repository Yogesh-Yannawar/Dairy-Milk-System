from django.db import models
from farmers.models import Farmer
from decimal import Decimal

class MilkCollection(models.Model):
    SHIFT_CHOICES = [('morning', 'Morning'), ('evening', 'Evening')]
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='collections')
    date = models.DateField()
    shift = models.CharField(max_length=10, choices=SHIFT_CHOICES)
    quantity = models.DecimalField(max_digits=8, decimal_places=2)
    fat = models.DecimalField(max_digits=4, decimal_places=1)
    snf = models.DecimalField(max_digits=4, decimal_places=1)
    rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Auto-calculate rate based on fat content
        base_rate = Decimal('25.00')
        fat_bonus = (Decimal(str(self.fat)) - Decimal('3.5')) * Decimal('2.0')
        snf_bonus = (Decimal(str(self.snf)) - Decimal('8.5')) * Decimal('1.5')
        self.rate = base_rate + fat_bonus + snf_bonus
        if self.rate < Decimal('15'):
            self.rate = Decimal('15')
        self.total_amount = Decimal(str(self.quantity)) * self.rate
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.farmer.name} - {self.date} - {self.shift}"

    class Meta:
        ordering = ['-date', '-shift']
        unique_together = ['farmer', 'date', 'shift']

class Inventory(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    unit = models.CharField(max_length=20)
    current_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    min_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_per_unit = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def is_low_stock(self):
        return self.current_stock <= self.min_stock

class InventoryTransaction(models.Model):
    TYPE_CHOICES = [('in', 'Stock In'), ('out', 'Stock Out')]
    item = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=5, choices=TYPE_CHOICES)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.transaction_type == 'in':
            self.item.current_stock += self.quantity
        else:
            self.item.current_stock -= self.quantity
        self.item.save()
