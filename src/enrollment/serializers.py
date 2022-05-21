import datetime

from rest_framework import serializers
from .models import Enrollments


class EnrollmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Enrollments
        fields = ['course', 'user', 'status']
