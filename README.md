# Reminder Scheduler API

A reminder scheduling backend built with Django REST Framework and Django Q. Authenticated users can create reminders with flexible frequency options — the backend automatically schedules background tasks to trigger each reminder at the right time.

---

## Features

- JWT authentication — register, login, token refresh
- Full reminder CRUD — create, list, retrieve, update, delete
- Frequency-based scheduling — once, hourly, daily, weekly, monthly
- Background task scheduling via Django Q
- Automatic task rescheduling when a reminder is updated
- Automatic task cancellation when a reminder is deleted
- User-scoped reminders — users only see and manage their own

---

## Tech Stack

- Python 3
- Django
- Django REST Framework
- djangorestframework-simplejwt
- Django Q (background task scheduling)
- SQLite

---

## Project Structure

```
scheduler/
├── reminders/
│   ├── models.py       # Reminder model
│   ├── views.py        # API views
│   ├── serializers.py  # DRF serializers
│   ├── tasks.py        # Django Q task scheduling logic
│   └── urls.py         # URL routes
└── manage.py
```

---

## Getting Started

### Installation

1. Clone the repository

```bash
git clone https://github.com/judesedem/AutoReminder.git
cd scheduler
```

2. Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Set up environment variables — create a `.env` file:

```
SECRET_KEY=your-secret-key
DEBUG=True
```

5. Run migrations

```bash
python manage.py migrate
```

6. Start the Django Q cluster (required for background tasks)

```bash
python manage.py qcluster
```

7. Start the server (in a separate terminal)

```bash
python manage.py runserver
```

---

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth required |
|--------|----------|-------------|---------------|
| POST | `/api/signup/` | Register a new user | No |
| POST | `/api/login/` | Login and receive JWT tokens | No |
| POST | `/api/token/refresh/` | Refresh access token | No |

### Reminders

| Method | Endpoint | Description | Auth required |
|--------|----------|-------------|---------------|
| GET | `/api/reminders/` | List your reminders | Yes |
| POST | `/api/reminders/` | Create a reminder | Yes |
| GET | `/api/reminders/<id>/` | Get a specific reminder | Yes |
| PUT/PATCH | `/api/reminders/<id>/` | Update a reminder | Yes |
| DELETE | `/api/reminders/<id>/` | Delete a reminder | Yes |

---

## Usage Example

### Login

```json
POST /api/login/
{
  "username": "jude",
  "password": "securepassword"
}
```

Response:
```json
{
  "Access": "<access_token>",
  "Refresh": "<refresh_token>",
  "user": {
    "id": 1,
    "username": "jude"
  }
}
```

### Create a reminder

```json
POST /api/reminders/
Authorization: Bearer <access_token>

{
  "title": "Take medication",
  "note": "After meals",
  "scheduled_time": "2026-06-01T08:00:00Z",
  "frequency": "D"
}
```

---

## Frequency Options

| Value | Label |
|-------|-------|
| `O` | Once |
| `H` | Hourly |
| `D` | Daily |
| `W` | Weekly |
| `M` | Monthly |

---

## How Scheduling Works

When a reminder is created or updated, `schedule_reminder_task()` is called automatically. It deletes any existing scheduled task for that reminder first, then registers a new one — preventing duplicate jobs.

When the reminder fires, `trigger_reminder()` runs in the background:

1. Fetches the reminder from the database
2. Posts a webhook payload to an external URL with the reminder details
3. If the reminder is recurring (daily, weekly, etc.), calculates the next occurrence and reschedules itself automatically
4. If it's a one-time reminder, it completes and stops

When a reminder is deleted, the corresponding Django Q schedule entry is cancelled — no orphaned background tasks.

This means the API doesn't just store reminders — it actively manages delivery, rescheduling, and cleanup as a fully automated background system.

---

## Author

**Jude Sedem**
GitHub: [@judesedem](https://github.com/judesedem)
Email: judesedem4@gmail.com
