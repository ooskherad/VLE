from django.db import models
from django.contrib.auth import get_user_model as user

from course.models import Courses
from home.models import Enumerations


class Instructor(models.Model):
    user = models.ForeignKey(to=user, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    about_you = models.TextField(null=True, default=None)


# todo:polymorphism model with https://django-polymorphic.readthedocs.io/en/stable/quickstart.html to offer other entity
class Offerings(models.Model):
    user = models.ForeignKey(to=user, on_delete=models.DO_NOTHING)
    entity_id = models.ForeignKey(to=Courses, on_delete=models.DO_NOTHING)
    entity_type = models.ForeignKey(to=Enumerations, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, default=None)
    meta_data = models.JSONField(null=True, default=None)
