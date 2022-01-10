from django.apps import AppConfig


class FxConfig(AppConfig):
    # default_auto_field = 'django.db.models.BigAutoField'
    name = 'fx'

    def ready(self):
        try:
            import fx.signals
        except ImportError:
            pass
