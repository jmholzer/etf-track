# Generated by Django 4.1 on 2022-08-29 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("etfs", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="measurement",
            name="expense_ratio",
        ),
        migrations.AddField(
            model_name="etf",
            name="expense_ratio",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="etf",
            name="sector",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]