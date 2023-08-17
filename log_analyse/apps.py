from django.apps import AppConfig


class LogAnalyseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'log_analyse'
    verbose_name = "Анализ лог файла CDN"
