from django.db import models

class Stat_settings (models.Model):
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    client_id = models.CharField(max_length=200)
    url_stat = models.CharField(max_length=200)
    url_auth = models.CharField(max_length=200)

class Portals_stat (models.Model):
    portal = models.CharField(max_length=200)
    id_portal = models.CharField(max_length=200)
    project = models.CharField(max_length=200)
    origin = models.CharField(max_length=200)
    old_project = models.BooleanField()
    def __str__(self) -> str:
        return self.portal