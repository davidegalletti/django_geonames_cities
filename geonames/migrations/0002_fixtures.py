# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from django.db import migrations
from django.core import management

logger = logging.getLogger(__name__)


def fixture_geonames(apps, schema_editor):
    try:
        pass
        # do nothing; it used to run commands that wouldn't work due to change in models that are
        # managed in following migrations
    except Exception as ex:
        logger.error("fixture_geonames: %s" % str(ex))


class Migration(migrations.Migration):

    dependencies = [
        ('geonames', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(fixture_geonames)
    ]
