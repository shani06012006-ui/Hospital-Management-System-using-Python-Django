from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView

from .models import Doctor, Patient, Appointment
from .forms import DoctorForm, PatientForm, AppointmentForm


class HomeView(TemplateView):
    """Dashboard showing overall hospital statistics."""
    template_name = 'hospital/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doctor_count'] = Doctor.objects.count()
        context['patient_count'] = Patient.objects.count()
        context['appointment_count'] = Appointment.objects.count()
        context['admitted_count'] = Patient.objects.filter(admitted=True).count()
        context['pending_appointments'] = Appointment.objects.filter(status='PEND').count()
        context['recent_appointments'] = Appointment.objects.select_related('patient', 'doctor')[:5]
        return context


# ---------------------- DOCTOR VIEWS ----------------------

class DoctorListView(ListView):
    model = Doctor
    template_name = 'hospital/doctor_list.html'
    context_object_name = 'doctors'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset


class DoctorCreateView(CreateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'hospital/doctor_form.html'
    success_url = reverse_lazy('doctor-list')

    def form_valid(self, form):
        messages.success(self.request, 'Doctor added successfully.')
        return super().form_valid(form)


class DoctorUpdateView(UpdateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'hospital/doctor_form.html'
    success_url = reverse_lazy('doctor-list')

    def form_valid(self, form):
        messages.success(self.request, 'Doctor updated successfully.')
        return super().form_valid(form)


class DoctorDeleteView(DeleteView):
    model = Doctor
    template_name = 'hospital/doctor_confirm_delete.html'
    success_url = reverse_lazy('doctor-list')

    def form_valid(self, form):
        messages.success(self.request, 'Doctor removed.')
        return super().form_valid(form)


# ---------------------- PATIENT VIEWS ----------------------

class PatientListView(ListView):
    model = Patient
    template_name = 'hospital/patient_list.html'
    context_object_name = 'patients'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset


class PatientCreateView(CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'hospital/patient_form.html'
    success_url = reverse_lazy('patient-list')

    def form_valid(self, form):
        messages.success(self.request, 'Patient registered successfully.')
        return super().form_valid(form)


class PatientUpdateView(UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'hospital/patient_form.html'
    success_url = reverse_lazy('patient-list')

    def form_valid(self, form):
        messages.success(self.request, 'Patient details updated.')
        return super().form_valid(form)


class PatientDeleteView(DeleteView):
    model = Patient
    template_name = 'hospital/patient_confirm_delete.html'
    success_url = reverse_lazy('patient-list')

    def form_valid(self, form):
        messages.success(self.request, 'Patient record removed.')
        return super().form_valid(form)


# ---------------------- APPOINTMENT VIEWS ----------------------

class AppointmentListView(ListView):
    model = Appointment
    template_name = 'hospital/appointment_list.html'
    context_object_name = 'appointments'
    paginate_by = 10

    def get_queryset(self):
        return Appointment.objects.select_related('patient', 'doctor')


class AppointmentCreateView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'hospital/appointment_form.html'
    success_url = reverse_lazy('appointment-list')

    def form_valid(self, form):
        messages.success(self.request, 'Appointment scheduled successfully.')
        return super().form_valid(form)


class AppointmentUpdateView(UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'hospital/appointment_form.html'
    success_url = reverse_lazy('appointment-list')

    def form_valid(self, form):
        messages.success(self.request, 'Appointment updated successfully.')
        return super().form_valid(form)


class AppointmentDeleteView(DeleteView):
    model = Appointment
    template_name = 'hospital/appointment_confirm_delete.html'
    success_url = reverse_lazy('appointment-list')

    def form_valid(self, form):
        messages.success(self.request, 'Appointment cancelled/removed.')
        return super().form_valid(form)
