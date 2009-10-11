import sys
import logging

from django.core.management.base import BaseCommand

from pypi_vanity.interface import Updater
from pypi_vanity.models import Package


class Command(BaseCommand):
    help = 'Updates package statistics from PyPI'

    def handle(self, **options):
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
        updater = Updater()
        updater.update_all()
