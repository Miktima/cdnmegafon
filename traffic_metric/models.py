from django.db import models

class Metric_settings (models.Model):
    url_metric = models.CharField(max_length=200)
    token = models.CharField(max_length=200)


class Metrics (models.Model):
    name = models.CharField(max_length=200)
    def __str__(self) -> str:
        return self.name

class Granularity (models.Model):
    nsec = models.IntegerField('number of seconds')
    code = models.CharField(max_length=50)
    def __str__(self) -> str:
        return str(self.nsec)