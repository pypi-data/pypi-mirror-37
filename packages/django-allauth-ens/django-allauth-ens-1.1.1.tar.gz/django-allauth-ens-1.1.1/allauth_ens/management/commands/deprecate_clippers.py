# coding: utf-8
from django.core.management.base import BaseCommand

from allauth_ens.adapter import deprecate_clippers


class Command(BaseCommand):
    help = 'Deprecates clipper SocialAccounts so as to avoid conflicts'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        deprecate_clippers()
        self.stdout.write(self.style.SUCCESS(
            'Clippers deprecation successful'))
