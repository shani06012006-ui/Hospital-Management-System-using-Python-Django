import logging

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import NoReverseMatch, reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import AppointmentForm, DoctorForm, PatientForm
from .models import Appointment, Doctor, Notification, Patient

logger = logging.getLogger(__name__)


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


# ---------------------- NOTIFICATION VIEWS ----------------------

class NotificationListView(ListView):
    """Full page listing every notification, newest first."""
    model = Notification
    template_name = 'hospital/notification_list.html'
    context_object_name = 'notifications'
    paginate_by = 20


def mark_notification_read(request, pk):
    """Mark a single notification as read, then redirect to its linked page (or back)."""
    notification = get_object_or_404(Notification, pk=pk)
    notification.is_read = True
    notification.save()

    if notification.link:
        try:
            return redirect(reverse(notification.link))
        except NoReverseMatch:
            logger.warning(
                "Notification %s has an invalid link '%s'; falling back to referrer.",
                notification.pk, notification.link,
            )
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def mark_all_notifications_read(request):
    """Mark every notification as read."""
    Notification.objects.filter(is_read=False).update(is_read=True)
    messages.success(request, 'All notifications marked as read.')
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def notifications_unread_api(request):
    """
    JSON endpoint polled by the navbar bell (via JavaScript) so notifications
    update live without a full page reload.
    """
    unread_count = Notification.objects.filter(is_read=False).count()
    latest = Notification.objects.all()[:8]
    data = {
        'unread_count': unread_count,
        'notifications': [
            {
                'id': n.id,
                'message': n.message,
                'is_read': n.is_read,
                'created_at': n.created_at.strftime('%b %d, %I:%M %p'),
                'link': n.link,
            }
            for n in latest
        ],
    }
    return JsonResponse(data)





