# Generated by Django 5.0 on 2023-12-27 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geonames', '0002_fixtures'),
    ]

    operations = [
        migrations.AddField(
            model_name='geonamesadm3',
            name='it_codice_istat',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]