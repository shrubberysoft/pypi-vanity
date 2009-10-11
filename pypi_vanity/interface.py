"""Thin abstraction over PyPI XML-RPC service."""

import logging
import xmlrpclib

from pypi_vanity.models import Package, Release, DownloadHistory

logger = logging.getLogger(__name__)
PYPI_URL = 'http://python.org/pypi'


class Updater(object):
    """Statistics updater."""

    def __init__(self):
        self.pypi = xmlrpclib.ServerProxy(PYPI_URL)

    def update_all(self):
        """Update statistics for all packages."""
        for package in Package.objects.all():
            self.update_package(package)

    def update_package(self, pkg):
        logger.info("Updating package %s", pkg.name)
        added, removed, current = self.get_releases(pkg)
        for version in added:
            logger.info("New release %s %s", pkg.name, version)
            release = pkg.releases.create(version=version)
        for version in removed:
            release = pkg.releases.get(version=version)
            release.delete()
            logger.warning("Version %s removed", version)
        self.update_releases(pkg)

    def update_releases(self, pkg):
        for release in pkg.releases.all():
            logger.info("Updating %s %s", pkg.name, release.version)
            urls = self.pypi.release_urls(pkg.name, release.version)
            downloads = sum(int(url['downloads']) for url in urls)
            release.download_history.create(total_downloads=downloads)
            release.total_downloads = downloads
            release.save()

    def get_releases(self, pkg):
        """Finds added, removed and current (already seen) releases for a
        given package."""
        remote = set(self.pypi.package_releases(pkg.name, pkg.track_hidden))
        local = set(pkg.releases.values_list('version', flat=True))
        added = remote.difference(local)
        removed = local.difference(remote)
        current = remote.intersection(local)
        return (added, removed, current)
