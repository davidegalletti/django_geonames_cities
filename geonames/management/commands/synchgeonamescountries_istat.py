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
        istat_ute_url = 'https://www.istat.it/wp-content/uploads/2024/03/Elenco-codici-e-denominazioni-unita-territoriali-estere.zip'
        # Let's import countries:
        try:
            # l'aggiornamento del codice istat da istat_ute_url non funziona perché l'elenco dei paesi non è
            # completo e alcuni codici degli stati non coincidono. Es: Codice ISO 3166 alpha2 UK su istat e GB su
            # geonames
            # usiamo una mappa dei codici
            map_istat_geonames_country_codes = { 
                'UK': 'GB' 
            }
            path_istat_countries = settings.GEONAMES_DEST_PATH + "istat_ute.zip"
            istat_downloader = Downloader(istat_ute_url, path_istat_countries)
            istat_downloader.download()
            csv_file = open(istat_downloader.single_file_if_zip(['csv', 'Elenco-codici-e-denominazioni']),
                            'rt', encoding='latin')
            csv_reader = csv.reader(csv_file, delimiter=';', quotechar="\\")
            for row in csv_reader:
                if row[0] == "S":
                    geonames_cc = row[11]
                    if row[11] in map_istat_geonames_country_codes:
                        geonames_cc = map_istat_geonames_country_codes[row[11]]
                    if Country.objects.filter(code=geonames_cc).exists():
                        c = Country.objects.get(code=geonames_cc)
                        c.it_codice_istat = '999%s' % row[5]
                        c.save()
        except Exception as ex:
            logger.error("Error %s" % str(ex))
