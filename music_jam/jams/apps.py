from django.apps import AppConfig

class JamsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'music_jam.jams'

    def ready(self):
        import music_jam.jams.signals