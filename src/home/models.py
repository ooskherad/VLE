from django.db import models
from django.contrib.auth import get_user_model as user


class Enumerations(models.Model):
    title = models.CharField(max_length=20)
    parent = models.ForeignKey(to="self", on_delete=models.CASCADE)
    created_by = models.ForeignKey(to=user, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
