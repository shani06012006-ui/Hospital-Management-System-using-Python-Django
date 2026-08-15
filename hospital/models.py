from django.db import models
from django.urls import reverse


class Doctor(models.Model):
    DEPARTMENT_CHOICES = [
        ('CARD', 'Cardiology'),
        ('NEURO', 'Neurology'),
        ('ORTHO', 'Orthopedics'),
        ('PEDS', 'Pediatrics'),
        ('GEN', 'General Medicine'),
        ('DERM', 'Dermatology'),
        ('ENT', 'ENT'),
        ('GYNO', 'Gynecology'),
    ]

    name = models.CharField(max_length=100)
    department = models.CharField(max_length=10, choices=DEPARTMENT_CHOICES, default='GEN')
    qualification = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"Dr. {self.name} ({self.get_department_display()})"

    def get_absolute_url(self):
        return reverse('doctor-list')


class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True)
    phone = models.CharField(max_length=15)
    address = models.TextField(blank=True)
    admitted = models.BooleanField(default=False)
    disease = models.CharField(max_length=200, blank=True, help_text="Diagnosis / reason for visit")
    registered_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-registered_on']

    def __str__(self):
        return f"{self.name} ({self.age}, {self.get_gender_display()})"

    def get_absolute_url(self):
        return reverse('patient-list')


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('PEND', 'Pending'),
        ('CONF', 'Confirmed'),
        ('DONE', 'Completed'),
        ('CANC', 'Cancelled'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    reason = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=4, choices=STATUS_CHOICES, default='PEND')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.patient.name} with Dr. {self.doctor.name} on {self.date}"

    def get_absolute_url(self):
        return reverse('appointment-list')
    

class Notification(models.Model):
    """A simple in-app notification, e.g. 'New appointment booked'."""

    TYPE_CHOICES = [
        ('APPT_NEW', 'New Appointment'),
        ('APPT_STATUS', 'Appointment Status Changed'),
        ('PATIENT_ADMIT', 'Patient Admitted'),
        ('GENERAL', 'General'),
    ]

    notif_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='GENERAL')
    message = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True, help_text="Optional URL name to redirect to")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.message
    
    