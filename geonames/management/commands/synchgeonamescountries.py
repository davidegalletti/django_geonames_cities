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
        downloader = Downloader()
        if downloader.download(
                source=base_url + "countryInfo.txt",
                destination=settings.GEONAMES_DEST_PATH + "countryInfo.txt",
                force=False
        ):
            # import the country file
            try:
                country_2b_deleted = [c['code'] for c in Country.objects.all().values('code')]
                with open(settings.GEONAMES_DEST_PATH + "countryInfo.txt", 'r') as geonames_file:
                    csv_reader = csv.reader(geonames_file, delimiter='\t', quotechar="\\")
                    for row in csv_reader:
                        if row[0][0] != "#":
                            if Country.objects.filter(code=row[0]).exists():
                                c = Country.objects.get(code=row[0])
                            else:
                                c = Country(code=row[0])
                            country_2b_deleted.remove(c.code)
                            c.name=row[4]
                            if c.code in municipality_levels.keys():
                                c.municipality_levels = municipality_levels[c.code]
                            c.save()
                            country_dict[row[0]] = c
                Country.objects.filter(code__in=country_2b_deleted).delete()
            except Exception as ex:
                logger.error("Error %s" % str(ex))
