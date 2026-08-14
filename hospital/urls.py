from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),

    # Doctors
    path('doctors/', views.DoctorListView.as_view(), name='doctor-list'),
    path('doctors/add/', views.DoctorCreateView.as_view(), name='doctor-add'),
    path('doctors/<int:pk>/edit/', views.DoctorUpdateView.as_view(), name='doctor-edit'),
    path('doctors/<int:pk>/delete/', views.DoctorDeleteView.as_view(), name='doctor-delete'),

    # Patients
    path('patients/', views.PatientListView.as_view(), name='patient-list'),
    path('patients/add/', views.PatientCreateView.as_view(), name='patient-add'),
    path('patients/<int:pk>/edit/', views.PatientUpdateView.as_view(), name='patient-edit'),
    path('patients/<int:pk>/delete/', views.PatientDeleteView.as_view(), name='patient-delete'),

    # Appointments
    path('appointments/', views.AppointmentListView.as_view(), name='appointment-list'),
    path('appointments/add/', views.AppointmentCreateView.as_view(), name='appointment-add'),
    path('appointments/<int:pk>/edit/', views.AppointmentUpdateView.as_view(), name='appointment-edit'),
    path('appointments/<int:pk>/delete/', views.AppointmentDeleteView.as_view(), name='appointment-delete'),
    
    # Notifications
    path('notifications/', views.NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/read/', views.mark_notification_read, name='notification-read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='notification-mark-all-read'),
    path('notifications/unread-api/', views.notifications_unread_api, name='notification-unread-api'),
]
