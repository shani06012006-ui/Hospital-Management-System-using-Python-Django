from django.contrib import admin
from .models import Doctor, Patient, Appointment


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'phone', 'experience_years', 'available')
    list_filter = ('department', 'available')
    search_fields = ('name', 'phone', 'email')


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'gender', 'blood_group', 'admitted', 'registered_on')
    list_filter = ('gender', 'admitted', 'blood_group')
    search_fields = ('name', 'phone')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'time', 'status')
    list_filter = ('status', 'date', 'doctor')
    search_fields = ('patient__name', 'doctor__name')
