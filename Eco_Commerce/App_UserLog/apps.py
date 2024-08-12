from django.apps import AppConfig



class AppUserlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'App_UserLog'

    def ready(self):
        import App_UserLog.signals
