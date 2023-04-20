from django.apps import AppConfig


class RentingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'renting'

    def ready(self):
        import renting.signals.handler
