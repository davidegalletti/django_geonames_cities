# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import json, logging
from datetime import datetime
from django.core.management.base import BaseCommand
from django.db.models import Q

from geonames.models import GeonamesAdm1, GeonamesAdm2, GeonamesAdm3, Country
from geonames.models import ItComuniCessati

from urllib.request import urlopen

logger = logging.getLogger(__name__)


def fixture_comuni_it_cessati():
    mappa_nomi = {
#        'Arzene': 'Basiliano',
#        'Montenars': 'Ragogna',
#        'Longano': 'Provvidenti',
#        "Macchia d'Isernia": 'Ripalimosani',
#        'Miranda': 'San Giacomo degli Schiavoni',
#        'Pesche': 'Trivento',
#        'Macchia Valfortore': 'Rotello',
#        'Camino di Codroipo': 'Cervignano del Friuli',
#        "Sant'Antonio Ruinas": 'Elmas',
#        "Acquaviva d'Isernia": 'Baranello',
#        'Belmonte del Sannio': 'Campobasso',
#        "Colle d'Anchise": 'Mafalda',
#        'Ferrazzano': 'Montagano',
#        'Mirabello Sannitico': 'San Felice del Molise',
#        'Oratino': 'Torella del Sannio',
#        'Corno di Rosazzo': 'Lestizza',
#        'Carlino': 'Codroipo',
#        'Chiauci': 'Lucito',
#        'Mutignano': 'Pineto',
#        'Santa Giusta': 'Quartucciu',
#        'Conca Casale': 'Molise',
#        'Monticelli di Borgogna': 'Montello',
#        'Fiumicello': 'Moggio Udinese',
#        'Nurachi': 'Sestu',
        'Casamicciola': 'Casamicciola Terme',
        'Avelengo/Hafling': 'Avelengo',
        'Velturno/Feldthurns': 'Velturno',
        'Saponara Villafranca': 'Saponara',
        'San Ponso Canavese': 'San Ponso',
        'Rodengo/Rodeneck': 'Rodengo',
        'Stelvio/Stilfs': 'Stelvio',
        'Colleretto Parella': 'Colleretto Giacosa',
        'Frignano Piccolo': 'Villa di Briano',
        'Palù': 'Palù del Fersina',
        'Torre Bairo': 'Torre Canavese',
        'Predoi/Prettau': 'Predoi',
        'Cerretto delle Langhe': 'Cerretto Langhe',
        'Calcerànica': 'Calceranica al Lago',
        'Andriano/Andrian': 'Andriano',
        'Campospinoso': 'Campospinoso Albaredo',
        'Buonanotte': 'Montebello sul Sangro',
        'Valdaora/Olang': 'Valdaora',
        'Fenis': 'Fénis',
        'Saint Marcel': 'Saint-Marcel',
        'Alì Marina': 'Alì Terme',
        'Lauregno/Laurein': 'Lauregno',
        'Proves/Proveis': 'Proves',
        'Arnaz': 'Arnad',
        'Castellania': 'Castellania Coppi',
        'Ruffrè': 'Ruffrè-Mendola',
        'Pettoranello di Molise': 'Pettoranello del Molise',
        'Gressoney la Trinité': 'Gressoney-La-Trinité',
        'Gressoney Saint Jean': 'Gressoney-Saint-Jean',
        'Albareto di Borgotaro': 'Albareto',
        "Cortina all'Adige/Kurtinig": 'Cortina sulla strada del vino',
        'Challant Saint Anselme': 'Challand-Saint-Anselme',
        'Challant Saint Victor': 'Challand-Saint-Victor',
        'La Valle/Wengen': 'La Valle',
        'Saint Denis': 'Saint-Denis',
        'Castel Verrino': 'Castelverrino',
        'Crandola': 'Crandola Valsassina',
        'Fai': 'Fai della Paganella',
        'Garniga': 'Garniga Terme',
        'Ronchi': 'Ronchi Valsugana',
        'Rhêmes Notre Dame': 'Rhêmes-Notre-Dame',
        'Rhêmes Saint Georges': 'Rhêmes-Saint-Georges',
        'Saint Nicolas': 'Saint-Nicolas',
        'Saint Pierre': 'Saint-Pierre',
        'Monasterolo Cassoto': 'Monasterolo Casotto',
        'Emarese': 'Emarèse',
        'Moniga': 'Moniga del Garda',
        'San Martino/St. Martin': 'San Martino in Passiria',
        'Saint Christophe': 'Saint-Christophe',
        'Castello': 'Castel Condino',
        'Pignola di Basilicata': 'Pignola',
        'Ollastra Simaxis': 'Ollastra',
        'Vauda di Front': 'Vauda Canavese',
        'Caderzone': 'Caderzone Terme',
        'Petruro': 'Petruro Irpino',
        'San Lorenzo di Mossa': 'San Lorenzo Isontino',
        'Saviore': "Saviore dell'Adamello",
        'San Giovanni di Bieda': 'Villa San Giovanni in Tuscia',
        'Ollastra Usellus': 'Albagiara',
        'Bannari di Usellus': 'Villa Verde',
        'San Pietro Pula': 'Villa San Pietro',
        'Campo di Calabria': 'Campo Calabro',
        'Castel Ritaldi e San Giovanni': 'Castel Ritaldi',
        'Rodi': 'Rodì Milici',
        'Soraga': 'Soraga di Fassa',
        'Campitello': 'Campitello di Fassa',
        'Anterivo/Altrei': 'Anterivo',
        'San Bartolomeo del Cervo': 'San Bartolomeo al Mare'
    }
    try:
        # https://situas-servizi.istat.it/publish/reportspooljson?pfun=98&pdatada=17/03/1861&pdataa=29/09/2025

        italy = Country.objects.get(code='IT')
        # creo se non esistenti adm2 e adm3 per comuni ASSORBITI in altra nazione
        vg, _ = GeonamesAdm1.objects.get_or_create(code='90',
                                                name='Compartimento statistico della Venezia Giulia',
                                                suppressed=True,
                                                country=italy)
        fu, _ = GeonamesAdm2.objects.get_or_create(code='FU', name='Fiume o del Carnaro', suppressed=True, adm1=vg)
        za, _ = GeonamesAdm2.objects.get_or_create(code='ZA', name='Zara', suppressed=True, adm1=vg)
        pl, _ = GeonamesAdm2.objects.get_or_create(code='PL', name='Pola', suppressed=True, adm1=vg)
        lb, _ = GeonamesAdm2.objects.get_or_create(code='LB', name='Lubiana', suppressed=True, adm1=vg)


        url_api = ('https://situas-servizi.istat.it/publish/reportspooljson?pfun=98&pdatada=17/03/1861&pdataa=%s' %
                   datetime.today().date().strftime('%d/%m/%Y'))
        comuni_cessati = urlopen(url_api).read()
        json_comuni_cessati = json.loads(comuni_cessati)
        mappa_nomi_trovati = {}
        for c in json_comuni_cessati["resultset"]:
            '''
            {
              "ANNO": 2024,
              "SIGLA_UTS": "VI",
              "COD_UTS": "024",
              "PRO_COM_T": "024044",
              "COD_CATASTO": "D902",
              "COMUNE": "Gambugliano",
              "COMUNE_A": null,
              "FLAG_ES_SCORPORO": null,
              "COD_VARIAZIONE": "ES",
              "DATA_INIZIO_AMMINISTRATIVA": "22\/01\/2024",
              "PRO_COM_T_REL": "024128",
              "COD_CATASTO_REL": "M436",
              "COMUNE_REL": "Sovizzo",
              "COD_UTS_REL": "024",
              "SIGLA_UTS_REL": "VI"
            }
            '''
            nome_comune = c['COMUNE']
            if c['COMUNE'] in mappa_nomi:
                nome_comune = mappa_nomi[c['COMUNE']]
            data_inizio = datetime.strptime(c['DATA_INIZIO_AMMINISTRATIVA'][:10], "%Y-%m-%d")
            codice_variazione = c['COD_VARIAZIONE']
            it_codice_catastale = c['COD_CATASTO']
            it_codice_istat = c['PRO_COM_T']
            if not ItComuniCessati.objects.filter(data_inizio=c['DATA_INIZIO_AMMINISTRATIVA'][:10], codice_variazione=codice_variazione,
                                                it_codice_catastale=it_codice_catastale).exists():
                cc = ItComuniCessati.objects.create(name=nome_comune,
                                                       data_inizio=data_inizio,
                                                       codice_variazione=codice_variazione,
                                                       it_codice_catastale=it_codice_catastale,
                                                       it_codice_istat=it_codice_istat,
                                                       sigla_provincia=c['SIGLA_UTS'],
                                                       name_rel=c['COMUNE_REL'],
                                                       it_codice_catastale_rel=(c['COD_UTS_REL'] if codice_variazione=='ES' else '')
                                                   )
            qs_and = GeonamesAdm3.objects.filter(name=nome_comune,
                                                 it_codice_catastale=c['COD_CATASTO'],
                                                 it_codice_istat=c['PRO_COM_T'])
            qs_or = GeonamesAdm3.objects.filter(Q(name=nome_comune) |
                                                Q(it_codice_catastale=c['COD_CATASTO']) |
                                                Q(it_codice_istat=c['PRO_COM_T']))
            if qs_and.exists() and qs_and.count() == 1:  # qs_and.exists() and qs_and.count()>1 non succede
                adm3 = qs_and.first()
                # adm3.suppressed = True
                # adm3.save()
                # logger.warning('%s adm3.id=%s TROVATO PER TUTTI I CRITERI' % (nome_comune,adm3.id))
            elif qs_or.exists():
                if qs_or.count() == 1:
                    adm3 = qs_or.first()
                    # adm3.suppressed = True
                    # adm3.save()
                    if adm3.name != nome_comune:
                        mappa_nomi_trovati[nome_comune] = adm3.name
                    quanti = (1 if adm3.name == nome_comune else 0)
                    quanti += (1 if adm3.it_codice_catastale == c['COD_CATASTO'] else 0)
                    quanti += (1 if adm3.it_codice_istat == c['PRO_COM_T'] else 0)
                    print('%s adm3.id=%s TROVATO 1 PER %s %s %s %s' % (
                        nome_comune,
                        adm3.id,
                        quanti,
                        ('name' if adm3.name == nome_comune else ('%s!=%s' % (adm3.name, nome_comune))),
                        ('it_codice_catastale' if adm3.it_codice_catastale == c['COD_CATASTO'] else (
                                    '%s!=%s' % (adm3.it_codice_catastale, c['COD_CATASTO']))),
                        ('it_codice_istat' if adm3.it_codice_istat==c['PRO_COM_T'] else (
                                '%s!=%s' % (adm3.it_codice_istat, c['PRO_COM_T'])))
                    ))
                else:
                    for adm3 in qs_or:
                        if adm3.name != nome_comune:
                            mappa_nomi_trovati[nome_comune] = adm3.name
                        quanti = (1 if adm3.name == nome_comune else 0)
                        quanti += (1 if adm3.it_codice_catastale == c['COD_CATASTO'] else 0)
                        quanti += (1 if adm3.it_codice_istat == c['PRO_COM_T'] else 0)
                        print('%s adm3.id=%s TROVATI %s per %s %s %s %s' % (
                            nome_comune,
                            adm3.id,
                            qs_or.count(),
                            quanti,
                            ('name' if adm3.name==nome_comune else ('%s!=%s' % (adm3.name, nome_comune))),
                            ('it_codice_catastale' if adm3.it_codice_catastale==c['COD_CATASTO'] else (
                                    '%s!=%s' % (adm3.it_codice_catastale, c['COD_CATASTO']))),
                            ('it_codice_istat' if adm3.it_codice_istat==c['PRO_COM_T'] else (
                                    '%s!=%s' % (adm3.it_codice_istat, c['PRO_COM_T'])))
                        ))
            elif 'SIGLA_UTS_REL' in c:
                qs_provincia = GeonamesAdm2.objects.filter(code=c['SIGLA_UTS_REL'])
                if qs_provincia.exists():
                    provincia = qs_provincia.first()
                    # creare nuovo record
                    # GeonamesAdm3.objects.create(name=nome_comune,
                    #                             code=' ',
                    #                             it_codice_catastale=c['COD_CATASTO'],
                    #                             it_codice_istat=c['PRO_COM_T'],
                    #                             adm2_id=provincia.id)
                else:
                    pass
                    # print('%s %s %s non trovato e provincia non trovata %s' % (nome_comune, c['COD_CATASTO'],
                    #                                                            c['PRO_COM_T'], c['SIGLA_UTS_REL']))

        for pr in GeonamesAdm2.objects.filter(adm1__country=italy):
            ItComuniCessati.objects.filter(sigla_provincia=pr.code).update(adm2=pr)
        print(mappa_nomi_trovati)
    except Exception as ex:
        logger.error("fixture_comuni_it_cessati: %s" % str(ex))
        raise Exception("fixture_comuni_it_cessati: %s" % str(ex))


class Command(BaseCommand):
    help = '''Fixtures
    '''

    def handle(self, *args, **options):
        try:
            fixture_comuni_it_cessati()
            print('FINITO')
        except Exception as ex:
            logger.error("fixture_comuni_it_cessati: %s" % str(ex))
