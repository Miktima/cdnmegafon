from django.db import models

class Cash_settings (models.Model):
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    url_auth = models.CharField(max_length=200)
    url_status = models.CharField(max_length=200)
    url_request = models.CharField(max_length=200)
