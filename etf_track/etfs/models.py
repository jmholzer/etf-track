from django.db import models


class ETF(models.Model):
    exchange = models.CharField(max_length=10)
    ticker = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    

class Measurement(models.Model):
    etf_id = models.PositiveIntegerField()
    date_time = models.DateTimeField()
