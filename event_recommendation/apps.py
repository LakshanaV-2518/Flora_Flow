from django.apps import AppConfig

class EventRecommendationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = 'event_recommendation'

    def ready(self):
        from .scheduler import start
        start()