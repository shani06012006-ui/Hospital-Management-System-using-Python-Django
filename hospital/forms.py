from django import forms

from .models import Appointment, Doctor, Patient


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'department', 'qualification', 'phone', 'email', 'experience_years', 'available']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full name'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. MBBS, MD'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'age', 'gender', 'blood_group', 'phone', 'address', 'admitted', 'disease']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full name'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'admitted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'disease': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Diagnosis / reason'}),
        }


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'date', 'time', 'reason', 'status']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'reason': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reason for visit'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
