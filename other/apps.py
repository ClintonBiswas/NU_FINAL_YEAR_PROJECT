from django.apps import AppConfig

class OtherConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'other'

    def ready(self):
        import other.signals  # Import signals.py to connect the signals
