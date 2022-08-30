from django.db import models


class ETF(models.Model):
    etf_issuer = models.CharField(max_length=255)
    ticker = models.CharField(max_length=10)
    exchange = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    sector = models.CharField(max_length=255, null=True, blank=True)
    expense_ratio = models.FloatField(null=True, blank=True)


class Measurement(models.Model):
    etf_id = models.PositiveIntegerField()
    date_time = models.DateTimeField()
    p_e = models.FloatField()
    ev_ebidta = models.FloatField()
