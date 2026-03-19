from django.db import models
from django.contrib.auth.models import User
from vendors.models import Vendor
# Create your models here.
class Issue(models.Model):

    STATUS_CHOICES = [
        ("Open","Open"),
        ("In Progress","In Progress"),
        ("Resolved","Resolved")
    ]

    SEVERITY_CHOICES = [
        ("Low","Low"),
        ("Medium","Medium"),
        ("High","High"),
        ("Critical","Critical")
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()

    severity = models.CharField(max_length=20,choices=SEVERITY_CHOICES)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="Open")

    assigned_to = models.ForeignKey(
    Vendor,
    on_delete=models.SET_NULL,
    null=True,
    blank=True
)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="creator")

    attachment = models.FileField(upload_to="issue_files/",
    null=True,
    blank=True)
    

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):

    issue = models.ForeignKey(Issue,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]