# Generated by Django 4.1 on 2022-08-21 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ETF',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exchange', models.CharField(max_length=10)),
                ('ticker', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=255)),
                ('sector', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etf_id', models.PositiveIntegerField()),
                ('date_time', models.DateTimeField()),
                ('p_e', models.FloatField()),
                ('ev_ebidta', models.FloatField()),
                ('expense_ratio', models.FloatField()),
            ],
        ),
    ]
