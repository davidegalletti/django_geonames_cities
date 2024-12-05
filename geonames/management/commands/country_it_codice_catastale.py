# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging

from geonames.models import Country
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


def fixture_country_it_codice_catastale():
    try:
        # https://www.istat.it/wp-content/uploads/2024/03/Elenco-codici-e-denominazioni-unita-territoriali-estere.zip
        Country.objects.get_or_create(code='--', name='APOLIDE', it_codice_catastale='Z999')
        Country.objects.filter(code='AL').update(it_codice_catastale='Z100')
        Country.objects.filter(code='AD').update(it_codice_catastale='Z101')
        Country.objects.filter(code='AT').update(it_codice_catastale='Z102')
        Country.objects.filter(code='BE').update(it_codice_catastale='Z103')
        Country.objects.filter(code='BG').update(it_codice_catastale='Z104')
        Country.objects.filter(code='DK').update(it_codice_catastale='Z107')
        Country.objects.filter(code='FO').update(it_codice_catastale='Z108')
        Country.objects.filter(code='FI').update(it_codice_catastale='Z109')
        Country.objects.filter(code='FR').update(it_codice_catastale='Z110')
        Country.objects.filter(code='DE').update(it_codice_catastale='Z112')
        Country.objects.filter(code='GI').update(it_codice_catastale='Z113')
        Country.objects.filter(code='GB').update(it_codice_catastale='Z114')
        Country.objects.filter(code='GR').update(it_codice_catastale='Z115')
        Country.objects.filter(code='IE').update(it_codice_catastale='Z116')
        Country.objects.filter(code='IS').update(it_codice_catastale='Z117')
        Country.objects.filter(code='CS').update(it_codice_catastale='Z118')
        Country.objects.filter(code='LI').update(it_codice_catastale='Z119')
        Country.objects.filter(code='LU').update(it_codice_catastale='Z120')
        Country.objects.filter(code='MT').update(it_codice_catastale='Z121')
        Country.objects.filter(code='IM').update(it_codice_catastale='Z122')
        Country.objects.filter(code='MC').update(it_codice_catastale='Z123')
        Country.objects.filter(code='NO').update(it_codice_catastale='Z125')
        Country.objects.filter(code='NL').update(it_codice_catastale='Z126')
        Country.objects.filter(code='PL').update(it_codice_catastale='Z127')
        Country.objects.filter(code='PT').update(it_codice_catastale='Z128')
        Country.objects.filter(code='RO').update(it_codice_catastale='Z129')
        Country.objects.filter(code='SM').update(it_codice_catastale='Z130')
        Country.objects.filter(code='ES').update(it_codice_catastale='Z131')
        Country.objects.filter(code='SE').update(it_codice_catastale='Z132')
        Country.objects.filter(code='CH').update(it_codice_catastale='Z133')
        Country.objects.filter(code='UA').update(it_codice_catastale='Z138')
        Country.objects.filter(code='HU').update(it_codice_catastale='Z134')
        Country.objects.filter(code='RU').update(it_codice_catastale='Z154')
        Country.objects.filter(code='VA').update(it_codice_catastale='Z106')
        Country.objects.filter(code='EE').update(it_codice_catastale='Z144')
        Country.objects.filter(code='LT').update(it_codice_catastale='Z146')
        Country.objects.filter(code='HR').update(it_codice_catastale='Z149')
        Country.objects.filter(code='SI').update(it_codice_catastale='Z150')
        Country.objects.filter(code='BA').update(it_codice_catastale='Z153')
        Country.objects.filter(code='MK').update(it_codice_catastale='Z148')
        Country.objects.filter(code='MD').update(it_codice_catastale='Z140')
        Country.objects.filter(code='SK').update(it_codice_catastale='Z155')
        Country.objects.filter(code='BY').update(it_codice_catastale='Z139')
        Country.objects.filter(code='CZ').update(it_codice_catastale='Z156')
        Country.objects.filter(code='ME').update(it_codice_catastale='Z159')
        Country.objects.filter(code='RS').update(it_codice_catastale='Z158')
        Country.objects.filter(code='XK').update(it_codice_catastale='Z160')
        Country.objects.filter(code='AF').update(it_codice_catastale='Z200')
        Country.objects.filter(code='SA').update(it_codice_catastale='Z203')
        Country.objects.filter(code='BH').update(it_codice_catastale='Z204')
        Country.objects.filter(code='BD').update(it_codice_catastale='Z249')
        Country.objects.filter(code='BT').update(it_codice_catastale='Z205')
        Country.objects.filter(code='MM').update(it_codice_catastale='Z206')
        Country.objects.filter(code='BN').update(it_codice_catastale='Z207')
        Country.objects.filter(code='KH').update(it_codice_catastale='Z208')
        Country.objects.filter(code='LK').update(it_codice_catastale='Z209')
        Country.objects.filter(code='CX').update(it_codice_catastale='Z702')
        Country.objects.filter(code='CN').update(it_codice_catastale='Z210')
        Country.objects.filter(code='CY').update(it_codice_catastale='Z211')
        Country.objects.filter(code='CC').update(it_codice_catastale='Z212')
        Country.objects.filter(code='KP').update(it_codice_catastale='Z214')
        Country.objects.filter(code='KR').update(it_codice_catastale='Z213')
        Country.objects.filter(code='AE').update(it_codice_catastale='Z215')
        Country.objects.filter(code='PH').update(it_codice_catastale='Z216')
        Country.objects.filter(code='PS').update(it_codice_catastale='Z218')
        Country.objects.filter(code='JP').update(it_codice_catastale='Z219')
        Country.objects.filter(code='JO').update(it_codice_catastale='Z220')
        Country.objects.filter(code='HK').update(it_codice_catastale='Z221')
        Country.objects.filter(code='IN').update(it_codice_catastale='Z222')
        Country.objects.filter(code='ID').update(it_codice_catastale='Z223')
        Country.objects.filter(code='IR').update(it_codice_catastale='Z224')
        Country.objects.filter(code='IQ').update(it_codice_catastale='Z225')
        Country.objects.filter(code='IL').update(it_codice_catastale='Z226')
        Country.objects.filter(code='KW').update(it_codice_catastale='Z227')
        Country.objects.filter(code='LA').update(it_codice_catastale='Z228')
        Country.objects.filter(code='LB').update(it_codice_catastale='Z229')
        Country.objects.filter(code='MO').update(it_codice_catastale='Z242')
        Country.objects.filter(code='MV').update(it_codice_catastale='Z232')
        Country.objects.filter(code='MY').update(it_codice_catastale='Z247')
        Country.objects.filter(code='MN').update(it_codice_catastale='Z233')
        Country.objects.filter(code='NP').update(it_codice_catastale='Z234')
        Country.objects.filter(code='OM').update(it_codice_catastale='Z235')
        Country.objects.filter(code='PK').update(it_codice_catastale='Z236')
        Country.objects.filter(code='QA').update(it_codice_catastale='Z237')
        Country.objects.filter(code='SG').update(it_codice_catastale='Z248')
        Country.objects.filter(code='SY').update(it_codice_catastale='Z240')
        Country.objects.filter(code='TH').update(it_codice_catastale='Z241')
        Country.objects.filter(code='TL').update(it_codice_catastale='Z242')
        Country.objects.filter(code='TR').update(it_codice_catastale='Z243')
        Country.objects.filter(code='VN').update(it_codice_catastale='Z251')
        Country.objects.filter(code='YE').update(it_codice_catastale='Z246')
        Country.objects.filter(code='KZ').update(it_codice_catastale='Z255')
        Country.objects.filter(code='UZ').update(it_codice_catastale='Z259')
        Country.objects.filter(code='AM').update(it_codice_catastale='Z252')
        Country.objects.filter(code='AZ').update(it_codice_catastale='Z253')
        Country.objects.filter(code='GE').update(it_codice_catastale='Z254')
        Country.objects.filter(code='KG').update(it_codice_catastale='Z256')
        Country.objects.filter(code='TJ').update(it_codice_catastale='Z257')
        Country.objects.filter(code='TW').update(it_codice_catastale='Z217')
        Country.objects.filter(code='TM').update(it_codice_catastale='Z258')
        Country.objects.filter(code='DZ').update(it_codice_catastale='Z301')
        Country.objects.filter(code='AO').update(it_codice_catastale='Z302')
        Country.objects.filter(code='CI').update(it_codice_catastale='Z313')
        Country.objects.filter(code='BJ').update(it_codice_catastale='Z314')
        Country.objects.filter(code='BW').update(it_codice_catastale='Z358')
        Country.objects.filter(code='BF').update(it_codice_catastale='Z354')
        Country.objects.filter(code='BI').update(it_codice_catastale='Z305')
        Country.objects.filter(code='CM').update(it_codice_catastale='Z306')
        Country.objects.filter(code='CV').update(it_codice_catastale='Z307')
        Country.objects.filter(code='CF').update(it_codice_catastale='Z308')
        Country.objects.filter(code='TD').update(it_codice_catastale='Z309')
        Country.objects.filter(code='KM').update(it_codice_catastale='Z310')
        Country.objects.filter(code='CG').update(it_codice_catastale='Z311')
        Country.objects.filter(code='EG').update(it_codice_catastale='Z336')
        Country.objects.filter(code='ET').update(it_codice_catastale='Z315')
        Country.objects.filter(code='GA').update(it_codice_catastale='Z316')
        Country.objects.filter(code='GM').update(it_codice_catastale='Z317')
        Country.objects.filter(code='GH').update(it_codice_catastale='Z318')
        Country.objects.filter(code='DJ').update(it_codice_catastale='Z361')
        Country.objects.filter(code='GN').update(it_codice_catastale='Z319')
        Country.objects.filter(code='GW').update(it_codice_catastale='Z320')
        Country.objects.filter(code='GQ').update(it_codice_catastale='Z321')
        Country.objects.filter(code='KE').update(it_codice_catastale='Z322')
        Country.objects.filter(code='LS').update(it_codice_catastale='Z359')
        Country.objects.filter(code='LR').update(it_codice_catastale='Z325')
        Country.objects.filter(code='LY').update(it_codice_catastale='Z326')
        Country.objects.filter(code='MG').update(it_codice_catastale='Z327')
        Country.objects.filter(code='MW').update(it_codice_catastale='Z328')
        Country.objects.filter(code='ML').update(it_codice_catastale='Z329')
        Country.objects.filter(code='MA').update(it_codice_catastale='Z330')
        Country.objects.filter(code='MR').update(it_codice_catastale='Z331')
        Country.objects.filter(code='MU').update(it_codice_catastale='Z332')
        Country.objects.filter(code='YT').update(it_codice_catastale='Z360')
        Country.objects.filter(code='MZ').update(it_codice_catastale='Z333')
        Country.objects.filter(code='NA').update(it_codice_catastale='Z300')
        Country.objects.filter(code='NE').update(it_codice_catastale='Z334')
        Country.objects.filter(code='NG').update(it_codice_catastale='Z335')
        Country.objects.filter(code='RE').update(it_codice_catastale='Z324')
        Country.objects.filter(code='RW').update(it_codice_catastale='Z338')
        Country.objects.filter(code='SH').update(it_codice_catastale='Z340')
        Country.objects.filter(code='ST').update(it_codice_catastale='Z341')
        Country.objects.filter(code='SC').update(it_codice_catastale='Z342')
        Country.objects.filter(code='SN').update(it_codice_catastale='Z343')
        Country.objects.filter(code='SL').update(it_codice_catastale='Z344')
        Country.objects.filter(code='SO').update(it_codice_catastale='Z345')
        Country.objects.filter(code='ZA').update(it_codice_catastale='Z347')
        Country.objects.filter(code='SD').update(it_codice_catastale='Z348')
        Country.objects.filter(code='SZ').update(it_codice_catastale='Z349')
        Country.objects.filter(code='TZ').update(it_codice_catastale='Z357')
        Country.objects.filter(code='TG').update(it_codice_catastale='Z351')
        Country.objects.filter(code='TN').update(it_codice_catastale='Z352')
        Country.objects.filter(code='UG').update(it_codice_catastale='Z353')
        Country.objects.filter(code='CD').update(it_codice_catastale='Z312')
        Country.objects.filter(code='ZM').update(it_codice_catastale='Z355')
        Country.objects.filter(code='ZW').update(it_codice_catastale='Z337')
        Country.objects.filter(code='ER').update(it_codice_catastale='Z368')
        Country.objects.filter(code='SS').update(it_codice_catastale='Z368')
        Country.objects.filter(code='AI').update(it_codice_catastale='Z529')
        Country.objects.filter(code='AG').update(it_codice_catastale='Z532')
        Country.objects.filter(code='AN').update(it_codice_catastale='Z501')
        Country.objects.filter(code='BS').update(it_codice_catastale='Z502')
        Country.objects.filter(code='BB').update(it_codice_catastale='Z522')
        Country.objects.filter(code='BZ').update(it_codice_catastale='Z512')
        Country.objects.filter(code='BM').update(it_codice_catastale='Z400')
        Country.objects.filter(code='CA').update(it_codice_catastale='Z401')
        Country.objects.filter(code='KY').update(it_codice_catastale='Z530')
        Country.objects.filter(code='CR').update(it_codice_catastale='Z503')
        Country.objects.filter(code='CU').update(it_codice_catastale='Z504')
        Country.objects.filter(code='DM').update(it_codice_catastale='Z526')
        Country.objects.filter(code='DO').update(it_codice_catastale='Z505')
        Country.objects.filter(code='SV').update(it_codice_catastale='Z506')
        Country.objects.filter(code='JM').update(it_codice_catastale='Z507')
        Country.objects.filter(code='GD').update(it_codice_catastale='Z524')
        Country.objects.filter(code='GL').update(it_codice_catastale='Z402')
        Country.objects.filter(code='GP').update(it_codice_catastale='Z508')
        Country.objects.filter(code='GT').update(it_codice_catastale='Z509')
        Country.objects.filter(code='HT').update(it_codice_catastale='Z510')
        Country.objects.filter(code='HN').update(it_codice_catastale='Z511')
        Country.objects.filter(code='MQ').update(it_codice_catastale='Z513')
        Country.objects.filter(code='MX').update(it_codice_catastale='Z514')
        Country.objects.filter(code='MS').update(it_codice_catastale='Z531')
        Country.objects.filter(code='NI').update(it_codice_catastale='Z515')
        Country.objects.filter(code='PA').update(it_codice_catastale='Z516')
        Country.objects.filter(code='PR').update(it_codice_catastale='Z518')
        Country.objects.filter(code='LC').update(it_codice_catastale='Z527')
        Country.objects.filter(code='VC').update(it_codice_catastale='Z528')
        Country.objects.filter(code='KN').update(it_codice_catastale='Z533')
        Country.objects.filter(code='PM').update(it_codice_catastale='Z403')
        Country.objects.filter(code='US').update(it_codice_catastale='Z404')
        Country.objects.filter(code='TC').update(it_codice_catastale='Z519')
        Country.objects.filter(code='VI').update(it_codice_catastale='Z520')
        Country.objects.filter(code='VG').update(it_codice_catastale='Z525')
        Country.objects.filter(code='AR').update(it_codice_catastale='Z600')
        Country.objects.filter(code='BO').update(it_codice_catastale='Z601')
        Country.objects.filter(code='BR').update(it_codice_catastale='Z602')
        Country.objects.filter(code='CL').update(it_codice_catastale='Z603')
        Country.objects.filter(code='CO').update(it_codice_catastale='Z604')
        Country.objects.filter(code='EC').update(it_codice_catastale='Z605')
        Country.objects.filter(code='FK').update(it_codice_catastale='Z609')
        Country.objects.filter(code='GY').update(it_codice_catastale='Z606')
        Country.objects.filter(code='GF').update(it_codice_catastale='Z607')
        Country.objects.filter(code='PY').update(it_codice_catastale='Z610')
        Country.objects.filter(code='PE').update(it_codice_catastale='Z611')
        Country.objects.filter(code='SR').update(it_codice_catastale='Z608')
        Country.objects.filter(code='TT').update(it_codice_catastale='Z612')
        Country.objects.filter(code='UY').update(it_codice_catastale='Z613')
        Country.objects.filter(code='VE').update(it_codice_catastale='Z614')
        Country.objects.filter(code='AU').update(it_codice_catastale='Z700')
        Country.objects.filter(code='CK').update(it_codice_catastale='Z703')
        Country.objects.filter(code='FJ').update(it_codice_catastale='Z704')
        Country.objects.filter(code='GU').update(it_codice_catastale='Z706')
        Country.objects.filter(code='KI').update(it_codice_catastale='Z731')
        Country.objects.filter(code='MP').update(it_codice_catastale='Z710')
        Country.objects.filter(code='MH').update(it_codice_catastale='Z711')
        Country.objects.filter(code='FM').update(it_codice_catastale='Z735')
        Country.objects.filter(code='NR').update(it_codice_catastale='Z713')
        Country.objects.filter(code='NU').update(it_codice_catastale='Z714')
        Country.objects.filter(code='NF').update(it_codice_catastale='Z715')
        Country.objects.filter(code='NC').update(it_codice_catastale='Z716')
        Country.objects.filter(code='NZ').update(it_codice_catastale='Z719')
        Country.objects.filter(code='PW').update(it_codice_catastale='Z734')
        Country.objects.filter(code='PG').update(it_codice_catastale='Z730')
        Country.objects.filter(code='PN').update(it_codice_catastale='Z722')
        Country.objects.filter(code='PF').update(it_codice_catastale='Z723')
        Country.objects.filter(code='SB').update(it_codice_catastale='Z724')
        Country.objects.filter(code='WS').update(it_codice_catastale='Z726')
        Country.objects.filter(code='TK').update(it_codice_catastale='Z727')
        Country.objects.filter(code='TO').update(it_codice_catastale='Z728')
        Country.objects.filter(code='TV').update(it_codice_catastale='Z732')
        Country.objects.filter(code='VU').update(it_codice_catastale='Z733')
        Country.objects.filter(code='WF').update(it_codice_catastale='Z729')

    except Exception as ex:
        logger.error("fixture_country_it_codice_catastale: %s" % str(ex))
        raise Exception("fixture_country_it_codice_catastale: %s" % str(ex))


class Command(BaseCommand):
    help = '''Fixtures
    '''

    def handle(self, *args, **options):
        try:
            fixture_country_it_codice_catastale()
        except Exception as ex:
            logger.error("fixture_country_it_codice_catastale: %s" % str(ex))
