# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging

from geonames.models import Country
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


def fixture_country_it_codice_catastale_cessati():
    try:
        # https://www.istat.it/wp-content/uploads/2011/01/Elenco-Paesi-esteri-cessati.zip
        Country.objects.get_or_create(code='YD', name='Yemen del Sud', it_codice_catastale='Z250')
        Country.objects.get_or_create(code='DD', name='Repubblica Democratica Tedesca', it_codice_catastale='Z111')
        Country.objects.get_or_create(code='SU', name='Unione Sovietica', it_codice_catastale='Z135')
        Country.objects.get_or_create(code='--', name='Cecoslovacchia', it_codice_catastale='Z105')
        Country.objects.get_or_create(code='YU', name='Repubblica Socialista Federale di Jugoslavia',
                                      it_codice_catastale='Z118')
        Country.objects.get_or_create(code='--', name='Serbia e Montenegro', it_codice_catastale='Z157')

    except Exception as ex:
        logger.error("fixture_country_it_codice_catastale_cessati: %s" % str(ex))
        raise Exception("fixture_country_it_codice_catastale_cessati: %s" % str(ex))


class Command(BaseCommand):
    help = '''Fixtures
    '''

    def handle(self, *args, **options):
        try:
            fixture_country_it_codice_catastale_cessati()
        except Exception as ex:
            logger.error("fixture_country_it_codice_catastale_cessati: %s" % str(ex))
