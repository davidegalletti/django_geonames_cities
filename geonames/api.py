import functools, json

from django.db.models import Q
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, JsonResponse
from importlib import import_module

from geonames.models import Country, GeonamesAdm1, GeonamesAdm2, GeonamesAdm3, \
    GeonamesAdm4, GeonamesAdm5, PopulatedPlace


def login_required_decorator(func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    def decorator(view_func):
        @functools.wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            return view_func(request, *args, **kwargs)


if hasattr(settings, "LOGIN_REQUIRED_MODULE") and hasattr(settings, "LOGIN_REQUIRED_DECORATOR"):
    lrm = import_module(getattr(settings, "LOGIN_REQUIRED_MODULE"))
    login_required_decorator = getattr(lrm, getattr(settings, "LOGIN_REQUIRED_DECORATOR"))


@login_required_decorator
def countries(request):
    try:
        q = request.GET.get('term', '')
        countries = Country.objects.filter(Q(name__icontains=q) | Q(alternate_names__icontains=q))
        results = []
        for c in countries:
            country_json = {
                'id': c.id,
                'label': c.name + ('(%s)' % c.alternate_names if c.alternate_names else ''),
                'code': c.code,
                'value': c.name + ('(%s)' % c.alternate_names if c.alternate_names else ''),
                'data_loaded': c.data_loaded,
                'nic_type': '',
                'nic_input_mask': '',
                'it_codice_catastale': c.it_codice_catastale
            }
            # if used with geonames_address ...
            if hasattr(c, 'nationalidentificationcodetype_set') and c.nationalidentificationcodetype_set.count() > 0:
                # TODO: we start with just one, make it a list and manage the choice of the type
                country_json['nic_type'] = c.nationalidentificationcodetype_set.all()[0].name
                country_json['nic_input_mask'] = c.nationalidentificationcodetype_set.all()[0].input_mask
            results.append(country_json)
    except:
        results = 'fail'
    return JsonResponse(results, safe=False)


@login_required_decorator
def municipalities(request):
    try:
        q = request.GET.get('term', '')
        country_id = request.GET.get('country_id', '')
        country = Country.objects.get(id=country_id)
        results = []
        content_types = []
        for ml in country.municipality_levels.split(" "):
            content_types.append(ContentType.objects.get(app_label='geonames', model__iexact=ml))
        municipalities = []
        exact_matches = []
        n_of_results = 20
        for ct in content_types:
            if ct.model == "geonamesadm1":
                exact_matches += GeonamesAdm1.objects.filter(name__iexact=q, country__id=country_id)[:n_of_results]
                municipalities += GeonamesAdm1.objects.filter(name__icontains=q, country__id=country_id)[:n_of_results]
            elif ct.model == "geonamesadm2":
                exact_matches += GeonamesAdm2.objects.filter(name__iexact=q, adm1__country__id=country_id)[
                                  :n_of_results]
                municipalities += GeonamesAdm2.objects.filter(name__icontains=q, adm1__country__id=country_id)[
                                  :n_of_results]
            elif ct.model == "geonamesadm3":
                exact_matches += GeonamesAdm3.objects.filter(name__iexact=q, adm2__adm1__country__id=country_id)[
                                  :n_of_results]
                municipalities += GeonamesAdm3.objects.filter(name__icontains=q, adm2__adm1__country__id=country_id)[
                                  :n_of_results]
            elif ct.model == "geonamesadm4":
                exact_matches += GeonamesAdm4.objects.filter(name__iexact=q, adm3__adm2__adm1__country__id=country_id)[
                                  :n_of_results]
                municipalities += GeonamesAdm4.objects.filter(name__icontains=q,
                                                              adm3__adm2__adm1__country__id=country_id)[:n_of_results]
            elif ct.model == "geonamesadm5":
                exact_matches += GeonamesAdm5.objects.filter(name__iexact=q,
                                                             adm4__adm3__adm2__adm1__country__id=country_id)[
                                  :n_of_results]
                municipalities += GeonamesAdm5.objects.filter(name__icontains=q,
                                                              adm4__adm3__adm2__adm1__country__id=country_id)[
                                  :n_of_results]
            elif ct.model == "populatedplace":
                exact_matches += PopulatedPlace.objects.filter(name__iexact=q, country__id=country_id)[:n_of_results]
                municipalities += PopulatedPlace.objects.filter(name__icontains=q, country__id=country_id)[
                                  :n_of_results]
        exact_matches.sort(key=lambda x: x.name)
        # TODO: if it starts with is to be prioritizes ws contains
        municipalities.sort(key=lambda x: x.name)
        # I remove duplicates
        for m in exact_matches:
            if m in municipalities:
                municipalities.remove(m)
        # if I have an exact match I send it as the first result;
        for m in exact_matches + municipalities:
            municipality_json = {}
            municipality_json['id'] = m.id
            municipality_json['label'] = m.name
            municipality_json['value'] = m.name
            municipality_json['content_type'] = ct.model
            municipality_json['content_type_id'] = ct.id
            if ct.model == "geonamesadm3" and country.code == 'IT':
                municipality_json['label'] = ("%s ( %s )" % (m.name, m.adm2.code))
                municipality_json['value'] = municipality_json['label']
                municipality_json['codice_catastale'] = m.it_codice_catastale
            results.append(municipality_json)
        data = json.dumps(results)
    except:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
