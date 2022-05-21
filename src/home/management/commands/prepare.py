import inspect
import sys

from django.core.management.base import BaseCommand
from django.db import connection

import home.enumerations
from accounts.models import User
from home.models import Enumerations
from home.models import FileGroup


class Command(BaseCommand):
    help = 'set enumerations'

    def handle(self, *args, **options):
        x = input('all tables will be truncate, are you sure? y/n: ')
        if x.lower() == 'y':
            truncate()
            self.stdout.write(self.style.SUCCESS('truncate tables successfully'))
        else:
            return

        user = User.objects.create_superuser(**{
            'mobile': '09372980101',
            'password': '1234',
            'name': 'سیستم',
            'email': 'admin@email.com'
        })
        for cls_name, cls_obj in inspect.getmembers(sys.modules['home.enumerations']):
            if inspect.isclass(cls_obj):
                members = cls_obj._member_map_
                if members.get('parent'):
                    members.pop('parent')
                    parent = Enumerations.objects.create(title=cls_obj.parent_name(), created_by=user)
                    for name, value in members.items():
                        Enumerations.objects.create(title=name.lower(), parent=parent, created_by=user)
                else:
                    if 'GroupFile' in cls_name:
                        for name, value in members.items():
                            FileGroup.objects.create(name=name.lower(), path=f'/{name.lower()}/')
        self.stdout.write(self.style.SUCCESS('system prepared successfully'))

    def add_arguments(self, parser):
        parser.add_argument(
            '-c',
            action='store_true',
            help='completely truncate tables',
        )


def truncate():
    tables = connection.introspection.table_names()
    seen_models = connection.introspection.installed_models(tables)
    step = 0
    for model in list(seen_models):
        step += 1
        print(f'truncating tables: {step} table', end="\r")
        connection.cursor().execute(f'TRUNCATE TABLE "{model._meta.db_table}" restart identity CASCADE')
