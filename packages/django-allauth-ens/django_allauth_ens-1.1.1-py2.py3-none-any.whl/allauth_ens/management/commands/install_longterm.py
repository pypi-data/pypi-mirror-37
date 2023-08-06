# coding: utf-8
from django.core.management.base import BaseCommand

from allauth_ens.adapter import install_longterm_adapter


class Command(BaseCommand):
    help = 'Manages the transition from an older django_cas' \
           'or an allauth_ens installation without ' \
           'LongTermClipperAccountAdapter'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fake',
            action='store_true',
            default=False,
            help=('Does not save the models created/updated,'
                  'only shows the list'),
        )
        pass

    def handle(self, *args, **options):
        logs = install_longterm_adapter(options.get("fake", False))
        self.stdout.write("Social accounts created : %d"
                          % len(logs["created"]))
        self.stdout.write("  ".join(("%s -> %s" % s) for s in logs["created"]))
        self.stdout.write("Social accounts displaced : %d"
                          % len(logs["updated"]))
        self.stdout.write("  ".join(("%s -> %s" % s) for s in logs["updated"]))
        self.stdout.write("User accounts unmodified : %d"
                          % len(logs["unmodified"]))
        self.stdout.write("   ".join(logs["unmodified"]))

        self.stdout.write(self.style.SUCCESS(
            "LongTermClipper migration successful"))
