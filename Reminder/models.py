from django.db import models
from account import User


class Reminder(models.Model):
    reminder=models.ForeignKey(User, on_delete=models.CASCADE)
    note=models.TextField(null=True, blank=True)
    title=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{ self.title}-{self.reminder}"