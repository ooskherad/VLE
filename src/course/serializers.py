from django.utils.text import slugify
from rest_framework import serializers
from django.db import transaction

from .models import *
from instructor.models import Instructor


class CourseSectionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    about_section = serializers.CharField()
    course_id = serializers.IntegerField()

    def create(self, validated_data):
        return CourseSections.objects.create(**validated_data)

    def update(self, instance, validated_data):
        pass


class CourseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    price = serializers.FloatField(default=0)
    level_id = serializers.IntegerField()
    categories = serializers.ListField(write_only=True)
    user_id = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        slug = validated_data.get('title')
        validated_data.update(slug=slugify(slug))
        categories = validated_data.pop('categories')
        user_id = validated_data.pop('user_id')
        with transaction.atomic():
            # todo: status
            course = Courses.objects.create(**validated_data)
            instructor = Instructor.objects.get(user_id=user_id)
            CourseOwners.objects.create(instructor=instructor, course=course)
            for category in categories:
                CourseCategories.objects.create(course=course, category_id=category)
        return course

    def update(self, instance, validated_data):
        pass


class CourseSubSectionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    course_section_id = serializers.IntegerField()

    def create(self, validated_data):
        return CourseSubSections.objects.create(**validated_data)

    def update(self, instance, validated_data):
        pass


class CourseSubSectionItemSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    course_sub_section_id = serializers.IntegerField()
    title = serializers.CharField()
    type_id = serializers.IntegerField()
    time_duration = serializers.IntegerField()
    price = serializers.FloatField(default=0)

    def create(self, validated_data):
        return CourseSubSectionItems.objects.create(**validated_data)

    def update(self, instance, validated_data):
        pass


class CourseSubSectionItemContentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    course_sub_section_item_id = serializers.IntegerField()
    content_type_id = serializers.IntegerField()
    content = serializers.CharField(default=None)

    def create(self, validated_data):
        return CourseSubSectionItemContent.objects.create(**validated_data)

    def update(self, instance, validated_data):
        pass
