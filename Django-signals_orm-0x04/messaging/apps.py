from django.apps import AppConfig

class ChatsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messging'

    def ready(self):
        import messaging.signals