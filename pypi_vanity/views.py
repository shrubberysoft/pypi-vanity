from django.template import RequestContext
from django.shortcuts import render_to_response

from pypi_vanity.models import Package


def package_index(request):
    context = RequestContext(request, dict(packages=Package.objects.all()))
    return render_to_response('vanity/package_index.html', context)
