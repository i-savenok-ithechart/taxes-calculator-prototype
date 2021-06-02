from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):

    def ready(self):
        try:
            # try to import signals.py file in the app dir if there is one
            __import__(f'{self.name}.signals')
        except ModuleNotFoundError:
            pass
