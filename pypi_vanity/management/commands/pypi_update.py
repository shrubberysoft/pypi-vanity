import sys
import logging

from django.core.management.base import BaseCommand

from pypi_vanity.interface import Updater
from pypi_vanity.models import Package


class Command(BaseCommand):
    help = 'Updates package statistics from PyPI'

    def handle(self, *args, **options):
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
        updater = Updater()
        if len(args):
            for name in args:
                package = Package.objects.get(name=name)
                updater.update_package(package)
        else:
            updater.update_all()
