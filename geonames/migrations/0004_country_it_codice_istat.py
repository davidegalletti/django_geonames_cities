# Generated by Django 5.0 on 2024-02-08 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geonames', '0003_geonamesadm3_it_codice_istat_alter_country_id_and_more'),
    ]


    operations = [
        migrations.AddField(
            model_name='country',
            name='it_codice_istat',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
    ]
