from django.db import models

# Create your models here.
from django.contrib.auth.models import User
class Vendor(models.Model):

    STATUS_CHOICES = [
        ("Active","Active"),
        ("Inactive","Inactive")
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200)

    email = models.EmailField()
    phone = models.CharField(max_length=20)

    contact_person = models.CharField(max_length=200)

    rating = models.FloatField(default=0)

    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="Active")

    joined_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name