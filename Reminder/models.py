from django.db import models
from django.contrib.auth import get_user_model

User=get_user_model()

class Reminder(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    note=models.TextField(blank=True, null=True)
    scheduled_time=models.DateTimeField()    
    FREQUENCY=[
        ('O','Once'), 
        ('D','Daily'),
        ('W','Weekly'),
        ('M','Monthly'),
        ('H','Hourly')
    ]
    frequency=models.CharField(max_length=1,choices=FREQUENCY)

    def __str__(self):
        return f"{self.title}-{self.scheduled_time}-{self.frequency}"