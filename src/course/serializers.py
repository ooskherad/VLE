from django.utils.text import slugify
from rest_framework import serializers
from django.db import transaction

from .models import *
from instructor.models import Instructor
from home.serializers import CategorySerializer, EnumerationSerializer


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            not_allowed = set(fields)
            for field_name in not_allowed:
                self.fields.pop(field_name)


class CourseOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseOwners
        fields = ['instructor', ]


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategories
        fields = ['category']

    def to_representation(self, instance):
        return {'id': instance.category.id, 'title': instance.category.title}


class CourseSubSectionItemContentSerializer(serializers.ModelSerializer):


    class Meta:
        model = CourseSubSectionItemContent
        fields = ['id', 'created_at', 'course_sub_section_item', 'content', 'content_type', 'file']


class CourseSubSectionItemSerializer(serializers.ModelSerializer):
    sub_section_item_content = CourseSubSectionItemContentSerializer(many=True, read_only=True)

    class Meta:
        model = CourseSubSectionItems
        fields = ['id', 'course_sub_section', 'title', 'type', 'time_duration', 'price', 'created_at',
                  'sub_section_item_content']

    def validate_time_duration(self, attrs):
        if attrs <= 0:
            raise serializers.ValidationError('time duration must an positive integer number (in second) ')
        return attrs


class CourseSubSectionSerializer(serializers.ModelSerializer):
    sub_section_item = CourseSubSectionItemSerializer(many=True, read_only=True)

    class Meta:
        model = CourseSubSections
        fields = ['id', 'course_section', 'title', 'created_at', 'sub_section_item']


class CourseSectionSerializer(serializers.ModelSerializer):
    sub_sections = CourseSubSectionSerializer(many=True, read_only=True)

    class Meta:
        model = CourseSections
        fields = ['id', 'course', 'title', 'about_section', 'created_at', 'sub_sections']


class CourseSerializer(DynamicFieldsModelSerializer):
    sections = CourseSectionSerializer(many=True, read_only=True)
    owners = CourseOwnerSerializer(many=True, write_only=True, required=False)
    categories = CourseCategorySerializer(many=True)
    level = serializers.StringRelatedField(read_only=True)
    level_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Enumerations.objects.all())
    image = serializers.CharField(required=False)

    class Meta:
        model = Courses
        fields = ['id', 'title', 'price', 'image', 'level_id', 'level', 'owners', 'categories', 'sections', ]

    def create(self, validated_data):
        owners = validated_data.pop('owners')
        categories = validated_data.pop('categories')
        with transaction.atomic():
            course = Courses.objects.create(**validated_data)
            for instructor in owners:
                CourseOwners.objects.create(course=course, instructor=instructor['instructor'])
            for category in categories:
                CourseCategories.objects.create(category=category['category'], course=course)

        return course
