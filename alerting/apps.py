from django.apps import AppConfig


class AlertingConfig(AppConfig):
    name = 'alerting'

    def ready(self):
        try:
            import alerting.signals
        except ImportError:
            pass
