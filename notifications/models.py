from django.db import models
from django.contrib.auth.models import User
from issue.models import Issue
# Create your models here.
class Notification(models.Model):

    TYPE_CHOICES = [
        ("issue_created","Issue Created"),
        ("comment_added","Comment Added"),
        ("status_updated","Status Updated"),
    ]

    user = models.ForeignKey(User,on_delete=models.CASCADE)

    issue = models.ForeignKey(Issue,on_delete=models.CASCADE)

    message = models.TextField()

    type = models.CharField(max_length=50,choices=TYPE_CHOICES)

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message