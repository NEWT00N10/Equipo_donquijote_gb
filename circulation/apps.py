from django.apps import AppConfig

class CirculationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "circulation"

    def ready(self):
        import circulation.signals  # noqa
