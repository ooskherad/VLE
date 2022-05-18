from rest_framework import serializers
from .models import Instructor
from accounts.models import User


class InstructorSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(write_only=True, queryset=User.objects.all())

    class Meta:
        model = Instructor
        fields = ['title', 'about_you', 'user', 'created_at']
