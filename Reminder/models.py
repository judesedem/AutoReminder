from django.db import models
from account import User
from django.utils import timezone

class Reminder(models.Model):
    reminder=models.ForeignKey(User, on_delete=models.CASCADE)
    note=models.TextField(null=True, blank=True)
    title=models.CharField(max_length=100)
    date_added=models.DateTimeField(default=timezone)

    def __str__(self):
        return self.title