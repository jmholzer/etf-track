# Generated by Django 4.1 on 2022-09-18 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ETF",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("etf_issuer", models.CharField(max_length=255)),
                ("ticker", models.CharField(max_length=10)),
                ("exchange", models.CharField(max_length=10)),
                ("name", models.CharField(max_length=255)),
                ("holdings_url", models.CharField(max_length=255)),
                ("sector", models.CharField(blank=True, max_length=255, null=True)),
                ("expense_ratio", models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Measurement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("etf_id", models.PositiveIntegerField()),
                ("date_time", models.DateTimeField()),
                ("p_e", models.FloatField()),
                ("ev_ebidta", models.FloatField()),
            ],
        ),
    ]
