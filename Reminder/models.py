from django.db import models
from django.contrib.auth.models import User

class Reminder(models.Model):
    note=models.TextField(null=True, blank=True)
    title=models.CharField(max_length=100)
    RemindItem=models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class ScheduleTime(models.Model):
    time=models.TimeField()
    reminder=models.ForeignKey(Reminder,on_delete=models.CASCADE,related_name='schedules')

    def __str__(self):
        return f"{self.reminder.title}-{self.time}"

class Interval(models.Model):
   FREQUENCY=[
       ('D','Daily'),
       ('W','Weekly'),
       ('M','Monthly'),
       ('H','Hourly'),
   ]
   frequency=models.CharField(max_length=1, choices=FREQUENCY)
   start_date=models.DateField()

   def __str__(self):
       return f"{self.frequency}-{self.start_time}"