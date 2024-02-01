# -*- coding: utf-8 -*-

import csv
import logging

from django.core.management.base import BaseCommand
from django.conf import settings

from geonames.downloader import Downloader

from geonames.models import Country

logger = logging.getLogger(__name__)


# municipality_levels is a dictionary that tells for some country which adm level holds the municipalities
# http://www.statoids.com/
from .synchgeonames import municipality_levels


class Command(BaseCommand):
    help = '''Synchronize countries data from GeoNames
    '''

    def handle(self, *args, **options):
        base_url = 'https://download.geonames.org/export/dump/'
        istat_ute_url = 'https://www.istat.it/it/files//2011/01/Elenco-codici-e-denominazioni-unita-territoriali-estere.zip'
        # Let's import countries:
        country_dict = {}
        path_countries = settings.GEONAMES_DEST_PATH + "countryInfo.txt"
        geonames_downloader = Downloader(base_url + "countryInfo.txt", path_countries)
        if geonames_downloader.download(force=False):
            # import the country file
            try:
                country_2b_deleted = [c['code'] for c in Country.objects.all().values('code')]
                with open(path_countries, 'r') as geonames_file:
                    csv_reader = csv.reader(geonames_file, delimiter='\t', quotechar="\\")
                    for row in csv_reader:
                        if row[0][0] != "#":
                            if Country.objects.filter(code=row[0]).exists():
                                c = Country.objects.get(code=row[0])
                            else:
                                c = Country(code=row[0])
                            if c.code in country_2b_deleted:
                                country_2b_deleted.remove(c.code)
                            c.name=row[4]
                            if c.code in municipality_levels.keys():
                                c.municipality_levels = municipality_levels[c.code]
                            c.save()
                            country_dict[row[0]] = c
                Country.objects.filter(code__in=country_2b_deleted).delete()
                # l'aggiornamento del codice istat da istat_ute_url non funziona perché l'elenco dei paesi non è
                # completo e alcuni codici degli stati non coincidono. Es: Codice ISO 3166 alpha2 UK su istat e GB su
                # geonames
                # path_istat_countries = settings.GEONAMES_DEST_PATH + "istat_ute.zip"
                # istat_downloader = Downloader(istat_ute_url, path_istat_countries)
                # istat_downloader.download()
                # csv_file = open(istat_downloader.single_file_if_zip(['csv', 'Elenco-codici-e-denominazioni']),
                #                 'rt', encoding='latin')
                # csv_reader = csv.reader(csv_file, delimiter=';', quotechar="\\")
                # for row in csv_reader:
                #     if row[0] == "S":
                #         if Country.objects.filter(code=row[11]).exists():
                #             c = Country.objects.get(code=row[11])
                #             c.it_codice_catastale = row[5]
                #             c.save()
            except Exception as ex:
                logger.error("Error %s" % str(ex))
