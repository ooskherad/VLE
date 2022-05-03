from django.core.management.base import BaseCommand
from home.models import Enumerations


class Command(BaseCommand):
    help = 'set enumerations'

    def handle(self, *args, **options):
        enums = Enumerations.objects.all()
        # todo : set enum and check new
