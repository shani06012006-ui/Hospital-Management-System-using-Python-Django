# Hospital Management System (Django Mini Project)

A simple full-stack Hospital Management System built with **Python + Django**.
It manages **Doctors**, **Patients**, and **Appointments** with full
Create / Read / Update / Delete (CRUD) functionality, a dashboard, and the
Django admin panel.

## Features

- Dashboard with live statistics (total doctors, patients, appointments, admitted patients)
- Doctor management (add, edit, delete, search, department, availability)
- Patient management (add, edit, delete, search, admission status, blood group)
- Appointment scheduling (link a patient with a doctor, date/time, status tracking)
- Django admin panel for quick backend management
- Clean, responsive UI (pure CSS, no external framework required)

## Project Structure

```
hospital_management/
├── manage.py
├── requirements.txt
├── README.md
├── hospital_management/        # Project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── hospital/                   # Main application
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── forms.py
    ├── views.py
    ├── urls.py
    ├── migrations/
    │   └── __init__.py
    ├── static/hospital/css/style.css
    └── templates/hospital/
        ├── base.html
        ├── home.html
        ├── doctor_list.html
        ├── doctor_form.html
        ├── doctor_confirm_delete.html
        ├── patient_list.html
        ├── patient_form.html
        ├── patient_confirm_delete.html
        ├── appointment_list.html
        ├── appointment_form.html
        └── appointment_confirm_delete.html
```

## Setup Instructions

1. **Create and activate a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Apply database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser** (to access /admin/)
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server**
   ```bash
   python manage.py runserver
   ```

6. **Open the app**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Models Overview

- **Doctor**: name, department, qualification, phone, email, experience_years, available
- **Patient**: name, age, gender, blood_group, phone, address, admitted, disease
- **Appointment**: patient (FK), doctor (FK), date, time, reason, status

## Notes

- Database used: SQLite (default, file `db.sqlite3` created automatically after migration).
- `DEBUG = True` and `SECRET_KEY` in `settings.py` are for development only —
  change them before deploying to production.
- This is a mini/academic project; there is no authentication/login system
  built in by default, but Django's admin login is available out of the box.
