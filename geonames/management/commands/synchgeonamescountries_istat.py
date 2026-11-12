# -*- coding: utf-8 -*-

import csv
import logging

from django.core.management.base import BaseCommand
from django.conf import settings

from geonames.downloader import Downloader

from geonames.models import Country

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = '''Synchronize countries data from GeoNames
    '''

    def handle(self, *args, **options):
        istat_ute_url = 'https://situas-servizi.istat.it/publish/reportspooljson?pfun=466&pdata=01/01/2001'
        try:
            path_istat_countries = settings.GEONAMES_DEST_PATH + "istat_ute.zip"
            istat_downloader = Downloader(istat_ute_url, path_istat_countries)
            istat_downloader.download()

            with open(path_istat_countries, 'r') as json_file:
                dati_ute = json.load(json_file)
            for row in dati_ute['resultset']:
                if "ISO_3166_ALPHA2" in row and Country.objects.filter(code=row["ISO_3166_ALPHA2"]).exists():
                    c = Country.objects.get(code=row["ISO_3166_ALPHA2"])
                    c.it_codice_istat = '999%s' % row["CODICE_ISTAT"]
                    c.save()
        except Exception as ex:
            logger.error("Error %s" % str(ex))
