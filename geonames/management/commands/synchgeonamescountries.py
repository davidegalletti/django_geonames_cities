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
        # Let's import countries:
        country_dict = {}
        path_countries = settings.GEONAMES_DEST_PATH + "countryInfo.txt"
        path_alternate_names = settings.GEONAMES_DEST_PATH + "alternateNamesV2.zip"
        geonames_downloader_country = Downloader(base_url + "countryInfo.txt", path_countries)
        geonames_downloader_alternate_names = Downloader(base_url + "alternateNamesV2.zip", path_alternate_names)
        alternate_language = settings.LANGUAGE_CODE[:2].lower()
        map_geonames_id_code = {}
        if geonames_downloader_country.download(force=False):
            # import the country file
            try:
                country_2b_deleted = [c['code'] for c in Country.objects.exclude(code='--').values('code')]
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
                            map_geonames_id_code[row[16]] = c.code
                            country_dict[row[0]] = c
                Country.objects.filter(code__in=country_2b_deleted).delete()
            except Exception as ex:
                logger.error("Error %s" % str(ex))
        if geonames_downloader_alternate_names.download(force=False) and alternate_language!='en':
            # unzip
            full_exctracted_path = geonames_downloader_alternate_names.single_file_if_zip('alternateNamesV2.txt')
            with open(full_exctracted_path, 'r') as geonames_file:
                csv_reader = csv.reader(geonames_file, delimiter='\t', quotechar="\\")
                for row in csv_reader:
                    if row[1] in map_geonames_id_code.keys() and row[2] == alternate_language:
                        c = Country.objects.get(code=map_geonames_id_code[row[1]])
                        c.alternate_names = row[3]
                        c.save()
