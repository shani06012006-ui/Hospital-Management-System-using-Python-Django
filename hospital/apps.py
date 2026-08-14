from django.apps import AppConfig


class HospitalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hospital'
    verbose_name = 'Hospital Management'
    
    def ready(self):
        import hospital.signals  # noqa: F401
