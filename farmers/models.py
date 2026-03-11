from django.db import models

class Farmer(models.Model):
    farmer_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    bank_name = models.CharField(max_length=100, blank=True)
    account_number = models.CharField(max_length=30, blank=True)
    ifsc_code = models.CharField(max_length=20, blank=True)
    joining_date = models.DateField()
    is_active = models.BooleanField(default=True)
    photo = models.ImageField(upload_to='farmers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.farmer_id} - {self.name}"

    class Meta:
        ordering = ['farmer_id']
