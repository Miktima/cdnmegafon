from django.apps import AppConfig


class LogAnalizeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'log_analize'
    verbose_name = "Анализ лог файла CDN"
