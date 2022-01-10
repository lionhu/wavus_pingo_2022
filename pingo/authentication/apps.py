from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    name = 'authentication'

    def ready(self):
        try:
            import authentication.signals
        except ImportError:
            pass
