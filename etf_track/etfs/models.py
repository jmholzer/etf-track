from django.db import models


class ETF(models.Model):
    etf_issuer = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    portfolio_url = models.CharField(max_length=255)
    holdings_url = models.CharField(max_length=255)
    sector = models.CharField(max_length=255, null=True, blank=True)
    expense_ratio = models.FloatField(null=True, blank=True)


class Measurement(models.Model):
    etf_id = models.PositiveIntegerField()
    date_time = models.DateTimeField()
    p_e = models.FloatField()
    ev_ebidta = models.FloatField()


class Holdings(models.Model):
    etf_id = models.PositiveBigIntegerField()
    ticker = models.CharField(max_length=14)
    percentage = models.FloatField()
