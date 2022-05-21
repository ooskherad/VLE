import inspect
import sys

from django.core.management.base import BaseCommand
from django.db import connection

import home.enumerations
from accounts.models import User
from home.models import Enumerations


class Command(BaseCommand):
    help = 'set enumerations'

    def handle(self, *args, **options):
        truncate()
        user = User.objects.create_user(**{
            'mobile': '09372980101',
            'password': '1234',
            'name': 'سیستم',
            'email': 'admin@email.com'
        })
        for cls_name, cls_obj in inspect.getmembers(sys.modules['home.enumerations']):
            if inspect.isclass(cls_obj):
                members = cls_obj._member_map_
                parent = Enumerations.objects.create(id=members.pop('parent').value, title=cls_obj.parent_name(),
                                                     created_by=user)
                for name, value in members.items():
                    Enumerations.objects.create(id=value.value, title=name.lower(), parent=parent, created_by=user)


def truncate():
    tables = connection.introspection.table_names()
    seen_models = connection.introspection.installed_models(tables)
    x = input('all tables will be truncate, are you sure? y/n: ')
    if x == 'n':
        return
    for model in list(seen_models):
        connection.cursor().execute(f'TRUNCATE TABLE "{model._meta.db_table}" restart identity CASCADE')
    print('truncate tables successfully')
