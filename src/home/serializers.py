from rest_framework import serializers

from accounts.serializers import UserSerializer
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.IntegerField(write_only=True, default=None)
    created_by = UserSerializer(write_only=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'parent', 'created_by']


class EnumerationSerializer(serializers.ModelSerializer):
    parent = serializers.IntegerField(write_only=True, default=None)
    created_by = UserSerializer(write_only=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'parent', 'created_by']
