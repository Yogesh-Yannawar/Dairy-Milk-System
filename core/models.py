from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('accountant', 'Accountant'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class MilkRate(models.Model):
    fat = models.DecimalField(max_digits=4, decimal_places=1)
    snf = models.DecimalField(max_digits=4, decimal_places=1)
    rate_per_liter = models.DecimalField(max_digits=8, decimal_places=2)
    effective_from = models.DateField()
    effective_to = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Fat:{self.fat} SNF:{self.snf} = ₹{self.rate_per_liter}"

    class Meta:
        ordering = ['-effective_from']
