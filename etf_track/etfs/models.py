from django.db import models


class ETF(models.Model):
    exchange = models.CharField(max_length=10)
    ticker = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    sector = models.CharField(max_length=255)


class Measurement(models.Model):
    etf_id = models.PositiveIntegerField()
    date_time = models.DateTimeField()
    p_e = models.FloatField()
    ev_ebidta = models.FloatField()
    expense_ratio = models.FloatField()    
