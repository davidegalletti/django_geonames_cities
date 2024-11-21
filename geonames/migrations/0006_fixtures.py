# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from django.db import migrations
from django.core import management

logger = logging.getLogger(__name__)


def fixture_geonames(apps, schema_editor):
    try:
        management.call_command('synchgeonamescountries')
        management.call_command('synchgeonames')
        management.call_command('country_it_codice_catastale')
        management.call_command('synchgeonamescountries_istat')
    except Exception as ex:
        logger.error("fixture_geonames: %s" % str(ex))


class Migration(migrations.Migration):

    dependencies = [
        ('geonames', '0005_alter_country_it_codice_istat'),
    ]

    operations = [
        migrations.RunPython(fixture_geonames)
    ]
