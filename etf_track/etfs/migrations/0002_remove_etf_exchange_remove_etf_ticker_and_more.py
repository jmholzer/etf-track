# Generated by Django 4.1 on 2022-09-19 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("etfs", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="etf",
            name="exchange",
        ),
        migrations.RemoveField(
            model_name="etf",
            name="ticker",
        ),
        migrations.AddField(
            model_name="etf",
            name="portfolio_url",
            field=models.CharField(default="a", max_length=255),
            preserve_default=False,
        ),
    ]
