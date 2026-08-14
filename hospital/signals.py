from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Appointment, Patient, Notification


@receiver(post_save, sender=Appointment)
def notify_on_appointment_save(sender, instance, created, **kwargs):
    """Create a notification whenever an appointment is booked or its status changes."""
    if created:
        Notification.objects.create(
            notif_type='APPT_NEW',
            message=f"New appointment: {instance.patient.name} with Dr. {instance.doctor.name} "
                     f"on {instance.date} at {instance.time}.",
            link='appointment-list',
        )
    else:
        Notification.objects.create(
            notif_type='APPT_STATUS',
            message=f"Appointment for {instance.patient.name} with Dr. {instance.doctor.name} "
                     f"is now '{instance.get_status_display()}'.",
            link='appointment-list',
        )


@receiver(pre_save, sender=Patient)
def track_previous_admitted_state(sender, instance, **kwargs):
    """Stash the previous 'admitted' value on the instance before it's saved."""
    if instance.pk:
        try:
            instance._previous_admitted = Patient.objects.get(pk=instance.pk).admitted
        except Patient.DoesNotExist:
            instance._previous_admitted = False
    else:
        instance._previous_admitted = False


@receiver(post_save, sender=Patient)
def notify_on_patient_admit(sender, instance, created, **kwargs):
    """Create a notification only when a patient transitions to admitted=True."""
    was_admitted = getattr(instance, '_previous_admitted', False)
    if instance.admitted and not was_admitted:
        Notification.objects.create(
            notif_type='PATIENT_ADMIT',
            message=f"Patient {instance.name} has been admitted.",
            link='patient-list',
        )