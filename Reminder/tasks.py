import requests
from datetime import timedelta
from django_q.tasks import schedule
from .models import Reminder

def trigger_reminder(reminder_id):
    try:
        reminder = Reminder.objects.get(id=reminder_id)

        webhook_url = "https://webhook.site/reminder1"
        
        payload = {
            "reminder_id": reminder.id,
            "title": reminder.title,
            "note": reminder.note,
            "scheduled_time": str(reminder.scheduled_time),
            "frequency": reminder.get_frequency_display(),
            "user": reminder.user.username
        }

        response = requests.post(webhook_url, json=payload)
        print(f"Reminder Triggered: {reminder.title} (Status: {response.status_code})")
        
        if reminder.frequency != 'O':
            next_time = calculate_next_occurrence(reminder)
            reminder.scheduled_time = next_time
            reminder.save()

            schedule_reminder_task(reminder)
            print(f"Rescheduled for: {next_time}")
        else:
            print(f" One-time reminder completed")
    
    except Reminder.DoesNotExist:
        print(f"Reminder {reminder_id} not found")
    except Exception as e:
        print(f"Error triggering reminder: {e}")


def calculate_next_occurrence(reminder):
    current_time = reminder.scheduled_time  
    
    if reminder.frequency == 'H':
        return current_time + timedelta(hours=1)
    elif reminder.frequency == 'D':
        return current_time + timedelta(days=1)
    elif reminder.frequency == 'W':
        return current_time + timedelta(weeks=1)
    elif reminder.frequency == 'M':
        return current_time + timedelta(days=30)
    
    return current_time


def schedule_reminder_task(reminder):
    schedule(
        'Reminder.tasks.trigger_reminder',  
        reminder.id,
        schedule_type='O',
        next_run=reminder.scheduled_time,
        name=f"reminder_{reminder.id}"
    )