# Generated by Django 4.1 on 2022-10-30 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("etfs", "0003_holdings"),
    ]

    operations = [
        migrations.CreateModel(
            name="Fundamentals",
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
                ("ticker", models.CharField(max_length=14)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                ("eps", models.FloatField(blank=True, null=True)),
            ],
        ),
    ]