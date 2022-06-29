from rest_framework import serializers

from accounts.models import User
from .models import Category, Enumerations


class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.IntegerField(write_only=True, default=None)
    created_by = serializers.PrimaryKeyRelatedField(write_only=True, queryset=User.objects.all())

    class Meta:
        model = Category
        fields = ['id', 'title', 'parent', 'created_by', 'icon']


class EnumerationSerializer(serializers.ModelSerializer):
    parent = serializers.IntegerField(write_only=True, default=None)
    created_by = serializers.PrimaryKeyRelatedField(write_only=True, queryset=User.objects.all())

    class Meta:
        model = Enumerations
        fields = ['id', 'title', 'parent', 'created_by']
