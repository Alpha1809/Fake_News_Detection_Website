from django.apps import AppConfig


class DetectorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'detector'
    
    def ready(self):
        # Import the ML model setup functionality
        from detector.utils import ml_model
        # Load the ML model when the app starts
        ml_model.init_model()
