from django.template import RequestContext
from django.shortcuts import render_to_response

from GChartWrapper import Pie, HorizontalBarStack
from pypi_vanity.models import Package


def package_index(request):
    packages = Package.with_statistics()
    packages_with_charts = [
        (package, build_package_chart(package)) for \
        package in packages
    ]
    context = RequestContext(request, {
        'packages': packages_with_charts,
        'summary_chart': build_summary_chart(packages),
    })
    return render_to_response('vanity/package_index.html', context)


def build_summary_chart(packages):
    downloads = [package.total_downloads for package in packages]
    names = [package.name for package in packages]
    if downloads:
        chart = HorizontalBarStack(downloads)
        chart.axes('y')
        chart.axes.label(0, *names[::-1])
        return chart
    return ''


def build_package_chart(package):
    releases = list(package.releases.order_by('-total_downloads')[:5])
    releases.sort(key=lambda r: r.version)
    downloads = [release.total_downloads for release in releases]
    if downloads:
        # Well, it seems that Google Charts cannot display value labels
        # (for pie charts, at least).
        versions = [ '%s (%s)' % (release.version, release.total_downloads) \
                     for release in releases ]
        title = '%s (%s)' % (package.name, package.total_downloads)
        return Pie(downloads).label(*versions).title(title)
    return ''
