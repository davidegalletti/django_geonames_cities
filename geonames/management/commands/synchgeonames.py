# -*- coding: utf-8 -*-

import csv
import logging

from zipfile import ZipFile

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Q

from geonames.downloader import Downloader

from geonames.models import Country, GeonamesAdm1, GeonamesAdm2, GeonamesAdm3, GeonamesAdm4, GeonamesAdm5, \
    PopulatedPlace

logger = logging.getLogger(__name__)

# municipality_levels is a dictionary that tells for some country which adm level holds the municipalities
# http://www.statoids.com/
municipality_levels = {
    'AD': 'GeonamesAdm1',
    'IT': 'GeonamesAdm3',
    'DK': 'GeonamesAdm2',
    'GB': 'PopulatedPlace',
    'FR': 'GeonamesAdm4',
    'NL': 'GeonamesAdm2',
    'BE': 'GeonamesAdm4',
    'ES': 'GeonamesAdm3',
    'PT': 'GeonamesAdm2',
    'HR': 'GeonamesAdm2',
    'DE': 'GeonamesAdm3',
    'CH': 'GeonamesAdm3',
}
if hasattr(settings, 'MUNICIPALITY_LEVELS'):
    municipality_levels.update(settings.MUNICIPALITY_LEVELS)

# m is a dictionary mapping Italian municipalities names for ISTAT into names for geonames
m = {
    # Uggiate con Ronago // Uggiate con Ronago    fusione del 1° gennaio 2024
    "Cornedo all'Isarco": "Cornedo all'Isarco/Karneid",
    # setteville
    'Popoli Terme': 'Popoli',  # ?
    # santa caterina deste
    "Savogna d'Isonzo": "Savogna d'Isonzo-Sovodnje ob Soči",
    'Duino Aurisina': 'Duino Aurisina-Devin Nabrežina',
    'Gais': 'Gais/Gais',
    'Lana': 'Lana/Lana',
    'Lasa': 'Lasa/Laas',
    'Montemagno Monferrato': 'Montemagno',
    'Ora': 'Ora/Auer',
    'Ortisei': 'Ortisei/St. Ulrich',
    'Parcines': 'Parcines/Partschins',
    'Postal': 'Postal/Burgstall',
    'Prato allo Stelvio': 'Prato allo Stelvio/Prad am Stilfserjoch',
    'Racines': 'Racines/Ratschings',
    'Rio di Pusteria': 'Rio di Pusteria/Mühlbach',
    'Rodengo': 'Rodengo/Rodeneck',
    'San Candido': 'San Candido/Innichen',
    'San Genesio Atesino': 'San Genesio Atesino/Jenesien',
    'San Leonardo in Passiria': 'San Leonardo in Passiria/St. Leonhard in Passeier',
    'San Lorenzo di Sebato': 'San Lorenzo di Sebato/St. Lorenzen',
    'San Martino in Badia': 'San Martino in Badia/St. Martin in Thurn',
    'Selva dei Molini': 'Selva dei Molini/Mühlwald',
    'Terento': 'Terento/Terenten',
    'Trodena nel parco naturale': 'Trodena nel parco naturale/Truden im Naturpark',
    'Tubre': 'Tubre/Taufers im Münstertal',
    'Varna': 'Varna/Vahrn',
    'Aldino': 'Aldino/Aldein',
    'Andriano': 'Andriano/Andrian',
    'Anterivo': 'Anterivo/Altrei',
    'Appiano sulla strada del vino': 'Appiano sulla strada del vino/Eppan an der Weinstraße',
    'Avelengo': 'Avelengo/Hafling',
    'Badia': 'Badia/Abtei',
    'Barbiano': 'Barbiano/Barbian',
    'Bolzano': 'Bolzano/Bozen',
    'Braies': 'Braies/Prags',
    'Brennero': 'Brennero/Brenner',
    'Bressanone': 'Bressanone/Brixen',
    'Bronzolo': 'Bronzolo/Branzoll',
    'Brunico': 'Brunico/Bruneck',
    'Caines': 'Caines/Kuens',
    'Caldaro sulla strada del vino': 'Caldaro sulla strada del vino/Kaltern an der Weinstraße',
    'Campo Tures': 'Campo Tures/Sand in Taufers',
    'Campo di Trens': 'Campo di Trens/Freienfeld',
    'Castelbello-Ciardes': 'Castelbello-Ciardes/Kastelbell-Tschars',
    'Castelrotto': 'Castelrotto/Kastelruth',
    'Cermes': 'Cermes/Tscherms',
    'Chienes': 'Chienes/Kiens',
    'Chiusa': 'Chiusa/Klausen',
    'Cortaccia sulla strada del vino': 'Cortaccia sulla strada del vino/Kurtatsch an der Weinstraße',
    'Cortina sulla strada del vino': 'Cortina sulla strada del vino/Kurtinig an der Weinstraße',
    'Corvara': 'Corvara in Badia/Corvara',
    'Curon Venosta': 'Curon Venosta/Graun im Vinschgau',
    'Dobbiaco': 'Dobbiaco/Toblach',
    'Doberdò del Lago': 'Doberdò del Lago-Doberdob',
    'Egna': 'Egna/Neumarkt',
    'Falzes': 'Falzes/Pfalzen',
    'Fiè allo Sciliar': 'Fiè allo Sciliar/Völs am Schlern',
    'Fortezza': 'Fortezza/Franzensfeste',
    'Funes': 'Funes/Villnöß',
    'Gargazzone': 'Gargazzone/Gargazon',
    'Glorenza': 'Glorenza/Glurns',
    'La Valle': 'La Valle/Wengen',
    'Laces': 'Laces/Latsch',
    'Lagundo': 'Lagundo/Algund',
    'Laion': 'Laion/Lajen',
    'Laives': 'Laives/Leifers',
    'Lauregno': 'Lauregno/Laurein',
    'Luson': 'Luson/Lüsen',
    'Magrè sulla strada del vino': 'Magrè sulla strada del vino/Margreid an der Weinstraße',
    'Malles Venosta': 'Malles Venosta/Mals',
    'Marebbe': 'Marebbe/Enneberg',
    'Marlengo': 'Marlengo/Marling',
    'Martello': 'Martello/Martell',
    'Meltina': 'Meltina/Mölten',
    'Merano': 'Merano/Meran',
    'Monguelfo-Tesido': 'Monguelfo-Tesido/Welsberg-Taisten',
    'Monrupino': 'Monrupino-Repentabor',
    'Montagna sulla strada del vino': 'Montagna sulla Strada del Vino/Montan an der Weinstraße',
    'Moso in Passiria': 'Moso in Passiria/Moos in Passeier',
    'Nalles': 'Nalles/Nals',
    'Naturno': 'Naturno/Naturns',
    'Naz-Sciaves': 'Naz-Sciaves/Natz-Schabs',
    'Nova Levante': 'Nova Levante/Welschnofen',
    'Nova Ponente': 'Nova Ponente/Deutschnofen',
    'Perca': 'Perca/Percha',
    'Plaus': 'Plaus/Plaus',
    'Ponte Gardena': 'Ponte Gardena/Waidbruck',
    'Predoi': 'Predoi/Prettau',
    'Proves': 'Proves/Proveis',
    'Rasun-Anterselva': 'Rasun-Anterselva/Rasen-Antholz',
    'Renon': 'Renon/Ritten',
    'Rifiano': 'Rifiano/Riffian',
    'Salorno sulla strada del vino': 'Salorno sulla strada del vino/Salurn an der Weinstraße',
    'San Dorligo della Valle': 'San Dorligo della Valle-Dolina',
    'San Floriano del Collio': 'San Floriano del Collio-Števerjan',
    'San Giovanni di Fassa': 'San Giovanni di Fassa-Sèn Jan',
    'San Martino in Passiria': 'San Martino in Passiria/St. Martin in Passeier',
    'San Pancrazio': 'San Pancrazio/St. Pankraz',
    'Santa Cristina Valgardena': 'Santa Cristina Valgardena/St. Christina in Gröden',
    'Sarentino': 'Sarentino/Sarntal',
    'Scena': 'Scena/Schenna',
    'Selva di Val Gardena': 'Selva di Val Gardena/Wolkenstein in Gröden',
    'Senale-San Felice': 'Senale-San Felice/Unsere Liebe Frau im Walde-St. Felix',
    'Senales': 'Senales/Schnals',
    'Sesto': 'Sesto/Sexten',
    'Sgonico': 'Sgonico-Zgonik',
    'Silandro': 'Silandro/Schlanders',
    'Sluderno': 'Sluderno/Schluderns',
    'Stelvio': 'Stelvio/Stilfs',
    'Terlano': 'Terlano/Terlan',
    'Termeno sulla strada del vino': 'Termeno sulla strada del vino/Tramin an der Weinstraße',
    'Tesimo': 'Tesimo/Tisens',
    'Tires': 'Tires/Tiers',
    'Tirolo': 'Tirolo/Tirol',
    'Ultimo': 'Ultimo/Ulten',
    'Vadena': 'Vadena/Pfatten',
    'Val di Vizze': 'Val di Vizze/Pfitsch',
    'Valdaora': 'Valdaora/Olang',
    'Valle Aurina': 'Valle Aurina/Ahrntal',
    'Valle di Casies': 'Valle di Casies/Gsies',
    'Vandoies': 'Vandoies/Vintl',
    'Velturno': 'Velturno/Feldthurns',
    'Verano': 'Verano/Vöran',
    'Villabassa': 'Villabassa/Niederdorf',
    'Villandro': 'Villandro/Villanders',
    'Vipiteno': 'Vipiteno/Sterzing',

}

GEONAMES_ADM_TYPES = ['ADM1', 'ADM2', 'ADM3', 'ADM4', 'ADM5']
GEONAMES_INCLUDE_CITY_TYPES = settings.GEONAMES_INCLUDE_CITY_TYPES if hasattr(settings, 'GEONAMES_INCLUDE_CITY_TYPES') \
    else []


class ICity:
    """
    City field indexes in geonames.
    Description of fields: https://download.geonames.org/export/dump/readme.txt
    """
    geonameid = 0
    name = 1
    asciiName = 2
    alternateNames = 3
    latitude = 4
    longitude = 5
    featureClass = 6
    featureCode = 7
    countryCode = 8
    cc2 = 9
    admin1Code = 10
    admin2Code = 11
    admin3Code = 12
    admin4Code = 13
    population = 14
    elevation = 15
    gtopo30 = 16
    timezone = 17
    modificationDate = 18


class IComuneItaliano:
    """
    ComuneItaliano field indexes in ISTAT.
    """
    Codice_Regione = 0
    Codice_unita_sovracomunale = 1
    Codice_Provincia_storico = 2
    Progressivo_del_Comune = 3
    Codice_Comune_formato_alfanumerico = 4
    Denominazione_italiana_e_straniera = 5
    Denominazione_in_italiano = 6
    Denominazione_altra_lingua = 7
    Codice_Ripartizione_Geografica = 8
    Ripartizione_geografica = 9
    Denominazione_regione = 10
    Denominazione_unita_sovracomunale = 11
    Sigla_automobilistica = 14
    Codice_Catastale_del_comune = 19


class Command(BaseCommand):
    help = '''Synchronize data from GeoNames
    '''

    def handle(self, *args, **options):
        log_every_n_records = 1000
        n_records = 0
        base_url = 'https://download.geonames.org/export/dump/'
        countries = settings.GEONAMES_INCLUDE_COUNTRIES if hasattr(settings, 'GEONAMES_INCLUDE_COUNTRIES') else []
        countries_excluded = settings.GEONAMES_EXCLUDE_INSERT_COUNTRIES \
            if hasattr(settings, 'GEONAMES_EXCLUDE_INSERT_COUNTRIES') else []
        # Let's create country dictionary to save some queries:
        country_dict = {}
        for c in Country.objects.filter(code__in=countries):
            country_dict[c.code] = c
        try:
            # download the files
            for c in countries:
                if c not in countries_excluded:
                    zip_path = settings.GEONAMES_DEST_PATH + c + ".zip"
                    downloader = Downloader(base_url + c + ".zip", zip_path)
                    if downloader.download(False):
                        # extract the file
                        with ZipFile(zip_path, 'r') as myzip:
                            myzip.extract(c + ".txt", settings.GEONAMES_DEST_PATH)
            # Let's import them
            logger.debug("synchgeonames countries_excluded %s" % countries_excluded)
            for c in countries:
                current_country_m_level = 0
                if municipality_levels[c] == 'PopulatedPlace':
                    current_country_m_level = 5
                elif municipality_levels[c][:len('GeonamesAdm')] == 'GeonamesAdm':
                    current_country_m_level = int(municipality_levels[c][len('GeonamesAdm'):])
                if current_country_m_level == 0:
                    logger.warning("Country %s has no setting for municipality level" % c.code)
                current_country = Country.objects.get(code=c)
                if (c not in countries_excluded):
                    logger.debug("synchgeonames importing %s %s" % (c, settings.GEONAMES_DEST_PATH + c + ".txt"))
                    with open(settings.GEONAMES_DEST_PATH + c + ".txt", 'r') as geonames_file:
                        csv_reader = csv.reader(geonames_file, delimiter='\t', quotechar="\\")
                        # Let's work on adm1 first
                        adm1_dict = {}
                        adm1_2b_deleted = []
                        for g in GeonamesAdm1.objects.filter(country_id=current_country.id).values('code'):
                            adm1_2b_deleted.append(g['code'])
                        for row in csv_reader:
                            if row[ICity.featureCode] in GEONAMES_ADM_TYPES and \
                                    row[ICity.featureCode] == 'ADM1' \
                                    and current_country_m_level >= 1:
                                if n_records % log_every_n_records == 0:
                                    logger.debug(
                                        "synchgeonames importing adm1 %s %s. %s records" % (
                                            row[ICity.countryCode], row[ICity.name], n_records))
                                n_records += 1
                                try:
                                    if GeonamesAdm1.objects.filter(code=row[ICity.admin1Code],
                                                                   country=country_dict[
                                                                       row[ICity.countryCode]]).exists():
                                        adm = GeonamesAdm1.objects.get(code=row[ICity.admin1Code],
                                                                       country=country_dict[row[ICity.countryCode]])
                                    else:
                                        adm = GeonamesAdm1(code=row[ICity.admin1Code],
                                                           country=country_dict[row[ICity.countryCode]])
                                    adm.name = row[ICity.name]
                                    adm.save()
                                    adm1_dict[row[ICity.admin1Code]] = adm
                                    try:
                                        adm1_2b_deleted.remove(adm.code)
                                    except ValueError as ex:
                                        pass
                                except Exception as ex:
                                    logger.error("Saving adm1 - %s - %s" % (str(ex), str(row)))
                        GeonamesAdm1.objects.filter(code__in=adm1_2b_deleted).delete()
                        # adm2
                        adm2_dict = {}
                        adm2_2b_deleted = []
                        for g in GeonamesAdm2.objects.filter(adm1__country_id=current_country.id).values('code'):
                            adm2_2b_deleted.append(g['code'])
                        geonames_file.seek(0)
                        for row in csv_reader:
                            if row[ICity.featureCode] in GEONAMES_ADM_TYPES and \
                                    row[ICity.featureCode] == 'ADM2' \
                                    and current_country_m_level >= 2:
                                if n_records % log_every_n_records == 0:
                                    logger.debug(
                                        "synchgeonames importing adm2 %s %s. %s records" % (
                                            row[ICity.countryCode], row[ICity.name], n_records))
                                n_records += 1
                                try:
                                    if GeonamesAdm2.objects.filter(code=row[ICity.admin2Code],
                                                                   adm1=adm1_dict[row[ICity.admin1Code]]).exists():
                                        adm = GeonamesAdm2.objects.get(code=row[ICity.admin2Code],
                                                                       adm1=adm1_dict[row[ICity.admin1Code]])
                                    else:
                                        adm = GeonamesAdm2(code=row[ICity.admin2Code],
                                                           adm1=adm1_dict[row[ICity.admin1Code]])
                                    adm.name = row[ICity.name]
                                    adm.save()
                                    adm2_dict[row[ICity.admin2Code]] = adm
                                    try:
                                        adm2_2b_deleted.remove(adm.code)
                                    except ValueError as ex:
                                        pass
                                except Exception as ex:
                                    logger.error("Saving adm2 - %s - %s" % (str(ex), str(row)))
                        GeonamesAdm2.objects.filter(code__in=adm2_2b_deleted).delete()
                        # adm3
                        adm3_dict = {}
                        adm3_2b_deleted = []
                        for g in GeonamesAdm3.objects.filter(adm2__adm1__country_id=current_country.id).values('code'):
                            adm3_2b_deleted.append(g['code'])
                        geonames_file.seek(0)
                        for row in csv_reader:
                            if row[ICity.featureCode] in GEONAMES_ADM_TYPES and \
                                    row[ICity.featureCode] == 'ADM3' \
                                    and current_country_m_level >= 3:
                                if n_records % log_every_n_records == 0:
                                    logger.debug(
                                        "synchgeonames importing adm3 %s %s. %s records" % (
                                            row[ICity.countryCode], row[ICity.name], n_records))
                                n_records += 1
                                try:
                                    if GeonamesAdm3.objects.filter(code=row[ICity.admin3Code],
                                                           adm2=adm2_dict[row[ICity.admin2Code]]).exists():
                                        adm = GeonamesAdm3.objects.get(code=row[ICity.admin3Code],
                                                           adm2=adm2_dict[row[ICity.admin2Code]])
                                    else:
                                        adm = GeonamesAdm3(code=row[ICity.admin3Code],
                                                           adm2=adm2_dict[row[ICity.admin2Code]])
                                    adm.name = row[ICity.name]
                                    adm.save()
                                    adm3_dict[row[ICity.admin3Code]] = adm
                                    try:
                                        adm3_2b_deleted.remove(adm.code)
                                    except ValueError as ex:
                                        pass
                                except Exception as ex:
                                    logger.error("Saving adm3 - %s - %s" % (str(ex), str(row)))
                        GeonamesAdm3.objects.filter(code__in=adm3_2b_deleted).delete()
                        # adm4
                        adm4_dict = {}
                        adm4_2b_deleted = []
                        for g in GeonamesAdm4.objects.filter(Q(adm2__adm1__country_id=current_country.id) | Q(
                                adm3__adm2__adm1__country_id=current_country.id)).values('code'):
                            adm4_2b_deleted.append(g['code'])
                        geonames_file.seek(0)
                        for row in csv_reader:
                            if row[ICity.featureCode] in GEONAMES_ADM_TYPES and \
                                    row[ICity.featureCode] == 'ADM4' \
                                    and current_country_m_level >= 4:
                                if n_records % log_every_n_records == 0:
                                    logger.debug(
                                        "synchgeonames importing adm4 %s %s. %s records" % (
                                            row[ICity.countryCode], row[ICity.name], n_records))
                                n_records += 1
                                try:
                                    if row[ICity.admin3Code]:
                                        if GeonamesAdm4.objects.filter(code=row[ICity.admin4Code],
                                                               adm3=adm3_dict[row[ICity.admin3Code]]).exists():
                                            adm = GeonamesAdm4.objects.get(code=row[ICity.admin4Code],
                                                               adm3=adm3_dict[row[ICity.admin3Code]])
                                        else:
                                            adm = GeonamesAdm4(code=row[ICity.admin4Code],
                                                               adm3=adm3_dict[row[ICity.admin3Code]])
                                        adm.name = row[ICity.name]
                                        adm.save()
                                        adm4_dict[row[ICity.admin4Code]] = adm
                                    elif row[ICity.admin2Code]:
                                        if GeonamesAdm4.objects.filter(code=row[ICity.admin4Code],
                                                               adm2=adm2_dict[row[ICity.admin2Code]]).exists():
                                            adm = GeonamesAdm4.objects.get(code=row[ICity.admin4Code],
                                                               adm2=adm2_dict[row[ICity.admin2Code]])
                                        else:
                                            adm = GeonamesAdm4(code=row[ICity.admin4Code],
                                                               adm2=adm2_dict[row[ICity.admin2Code]])
                                        adm.name = row[ICity.name]
                                        adm.save()
                                        adm4_dict[row[ICity.admin4Code]] = adm
                                    else:
                                        logger.warning("%s %s %s has neither admin3Code nor admin2Code" %
                                                       (row[ICity.name], row[ICity.featureCode], row[ICity.admin4Code]))
                                    try:
                                        adm4_2b_deleted.remove(adm.code)
                                    except ValueError as ex:
                                        pass
                                except Exception as ex:
                                    logger.error("Saving adm4 - %s - %s" % (str(ex), str(row)))
                        GeonamesAdm4.objects.filter(code__in=adm4_2b_deleted).delete()
                        # adm5
                        geonames_file.seek(0)
                        adm5_2b_deleted = []
                        for g in GeonamesAdm5.objects.filter(Q(adm4__adm2__adm1__country_id=current_country.id) | Q(
                                adm4__adm3__adm2__adm1__country_id=current_country.id)).values('name'):
                            adm5_2b_deleted.append(g['name'])
                        for row in csv_reader:
                            if row[ICity.featureCode] in GEONAMES_ADM_TYPES and \
                                    row[ICity.featureCode] == 'ADM5' \
                                    and current_country_m_level >= 5:
                                if n_records % log_every_n_records == 0:
                                    logger.debug(
                                        "synchgeonames importing adm5 %s %s. %s records" % (
                                            row[ICity.countryCode], row[ICity.name], n_records))
                                n_records += 1
                                try:
                                    if GeonamesAdm5.objects.filter(adm4=adm4_dict[row[ICity.admin4Code]]).exists():
                                        adm = GeonamesAdm5.objects.get(adm4=adm4_dict[row[ICity.admin4Code]])
                                    else:
                                        adm = GeonamesAdm5(adm4=adm4_dict[row[ICity.admin4Code]])
                                    adm.name = row[ICity.name]
                                    adm.save()
                                    try:
                                        adm5_2b_deleted.remove(adm.name)
                                    except ValueError as ex:
                                        pass
                                except Exception as ex:
                                    logger.error("Saving adm5 - %s - %s" % (str(ex), str(row)))
                        GeonamesAdm5.objects.filter(name__in=adm5_2b_deleted).delete()
                        # populated places
                        geonames_file.seek(0)
                        pp_2b_deleted = []
                        for g in PopulatedPlace.objects.filter(Q(adm1__country_id=current_country.id) |
                                           Q(adm2__adm1__country_id=current_country.id) |
                                           Q(adm3__adm2__adm1__country_id=current_country.id) |
                                           Q(adm4__adm3__adm2__adm1__country_id=current_country.id) |
                                           Q(adm4__adm2__adm1__country_id=current_country.id)).values('feature_code'):
                            pp_2b_deleted.append(g['feature_code'])
                        for row in csv_reader:
                            if row[ICity.featureCode] in GEONAMES_INCLUDE_CITY_TYPES \
                                    and current_country_m_level >= 5:
                                if n_records % log_every_n_records == 0:
                                    logger.debug(
                                        "synchgeonames importing ppl %s %s. %s records" % (
                                            row[ICity.countryCode], row[ICity.name], n_records))
                                n_records += 1
                                try:
                                    if PopulatedPlace.objects.filter(feature_code=row[ICity.featureCode],
                                                            country=country_dict[row[ICity.countryCode]]).exists():
                                        pp = PopulatedPlace.objects.get(feature_code=row[ICity.featureCode],
                                                            country=country_dict[row[ICity.countryCode]])
                                    else:
                                        pp = PopulatedPlace(feature_code=row[ICity.featureCode],
                                                            country=country_dict[row[ICity.countryCode]])
                                    pp.name = row[ICity.name]
                                    if row[ICity.admin1Code]:
                                        try:
                                            pp.adm1 = adm1_dict[row[ICity.admin1Code]]
                                        except:
                                            pass
                                    if row[ICity.admin2Code]:
                                        try:
                                            pp.adm2 = adm2_dict[row[ICity.admin2Code]]
                                        except:
                                            pass
                                    if row[ICity.admin3Code]:
                                        try:
                                            pp.adm3 = adm3_dict[row[ICity.admin3Code]]
                                        except:
                                            pass
                                    if row[ICity.admin4Code]:
                                        try:
                                            pp.adm4 = adm4_dict[row[ICity.admin4Code]]
                                        except:
                                            pass
                                    pp.save()
                                    try:
                                        pp_2b_deleted.remove(adm.feature_code)
                                    except ValueError as ex:
                                        pass
                                except Exception as ex:
                                    logger.error("Saving PopulatedPlace - %s - %s" % (str(ex), str(row)))
                        PopulatedPlace.objects.filter(feature_code__in=pp_2b_deleted).delete()

                        current_country.data_loaded = True
                        current_country.save()
                if c == 'IT' and c not in countries_excluded:
                    '''
                    '   I use the permalink to the ISTAT list of Italian municipalities to add to adm3 the field 
                    '   Codice Catastale
                    '''
                    istat_permalink = "https://www.istat.it/storage/codici-unita-amministrative/Elenco-comuni-italiani.csv"
                    path_comuni_it = settings.GEONAMES_DEST_PATH + "Elenco-comuni-italiani.csv"
                    downloader = Downloader(istat_permalink, path_comuni_it)
                    if downloader.download(False):
                        with open(path_comuni_it, 'r',
                                  encoding="ISO-8859-1") as istat_file:
                            csv_reader = csv.reader(istat_file, delimiter=';', quotechar="\\")
                            digits_as_string = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
                            for row in csv_reader:
                                # Let's loop on data from ISTAT
                                # if first column value is a number
                                if len(row[0]) and row[0][0] in digits_as_string:
                                    # and search on existing geonames records
                                    '''
                                    '   Year 2017, Sardinian towns have changed province, we try filtering just on names
                                    '   if we find more than one record we also filter on province (this case won't work
                                    '   with Sardinian towns, that's why we try it as a second option)
                                    '''
                                    # Some italian names are different so there is a mapping dictionary
                                    italian_name = row[IComuneItaliano.Denominazione_in_italiano]
                                    if italian_name in m.keys() and m[italian_name] != "":
                                        italian_name = m[italian_name]
                                    if GeonamesAdm3.objects.filter(
                                            Q(name=italian_name) |
                                            Q(name=row[IComuneItaliano.Denominazione_altra_lingua])
                                    ).exists():
                                        try:
                                            if GeonamesAdm3.objects.filter(
                                                    Q(name=italian_name) |
                                                    Q(name=row[IComuneItaliano.Denominazione_altra_lingua])
                                            ).count() == 1:
                                                adm3 = GeonamesAdm3.objects.get(
                                                    Q(name=italian_name) |
                                                    Q(name=row[IComuneItaliano.Denominazione_altra_lingua])
                                                )
                                            else:
                                                adm3 = GeonamesAdm3.objects.filter(
                                                    Q(name=italian_name) |
                                                    Q(name=row[IComuneItaliano.Denominazione_altra_lingua])
                                                ).get(adm2__code=row[IComuneItaliano.Sigla_automobilistica])
                                            adm3.name = row[IComuneItaliano.Denominazione_in_italiano]
                                            # Let's use ISTAT names ( geonames has Genoa instead of Genova, ISTAT has
                                            # it right )
                                            adm3.it_codice_catastale = row[IComuneItaliano.Codice_Catastale_del_comune]
                                            adm3.it_codice_istat = row[IComuneItaliano.Codice_Comune_formato_alfanumerico].zfill(5)
                                            adm3.save()
                                        except Exception as ex:
                                            logger.error(
                                                "%s//%s is in ISTAT's Elenco-comuni-italiani.csv. In Adm3 gave error: %s"
                                                % (italian_name,
                                                   row[IComuneItaliano.Denominazione_altra_lingua], str(ex)))
                                    else:
                                        logger.warning("%s//%s is in ISTAT's Elenco-comuni-italiani.csv but not in Adm3"
                                                       % (row[IComuneItaliano.Denominazione_in_italiano],
                                                          italian_name))


        except Exception as ex:
            logger.error("Error %s - %s" % (str(ex), str(row)))
        pass
