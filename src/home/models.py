from django.db import models
from accounts.models import User


class Category(models.Model):
    title = models.CharField(max_length=20)
    parent = models.ForeignKey(to="self", on_delete=models.CASCADE, null=True)
    icon = models.ImageField(default='category_icon.jpeg')
    created_by = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)


class Enumerations(models.Model):
    title = models.CharField(max_length=20)
    parent = models.ForeignKey(to="self", on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class FileGroup(models.Model):
    class Meta:
        db_table = 'file_group'

    name = models.CharField(max_length=30)
    path = models.CharField(max_length=30)


class Files(models.Model):
    type = models.CharField(max_length=20)
    format = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    size = models.IntegerField()
    group = models.ForeignKey(to=FileGroup, on_delete=models.CASCADE)
    created_by = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, default=None)

    def __str__(self):
        return self.title
