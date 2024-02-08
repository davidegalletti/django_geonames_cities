from django.http import HttpResponse
from django.urls import reverse


def test1(request):
    from django.core import management
    management.call_command('synchgeonamescountries_istat')
    # management.call_command('synchgeonames')

    from django.test import Client
    client = Client()
    response = client.get('%s://%s%s%s' % (
        request.META['SERVER_PROTOCOL'][:request.META['SERVER_PROTOCOL'].find('/')],
        request.META['HTTP_HOST'],
        reverse('geonames:municipalities'),
        '?term=AnDor&country_id=1'))
    return HttpResponse(response.status_code)
