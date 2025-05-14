from django.apps import AppConfig


class FinanceTrackerAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'finance_tracker_app'

    def ready(self):
        from .signals import create_profile, save_profile
