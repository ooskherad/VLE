from django.db import models

from home.models import Enumerations, Files, Category
from accounts.models import User


class Courses(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    price = models.FloatField(default=0)
    level = models.ForeignKey(to=Enumerations, on_delete=models.DO_NOTHING)
    image = models.ImageField(default='course_default.jpeg')
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, default=None)
    updated_at = models.DateTimeField(auto_now=True)

    def course_sections_relations(self):
        pass


class CourseCategories(models.Model):
    class Meta:
        db_table = 'course_categories'

    course = models.ForeignKey(to=Courses, on_delete=models.DO_NOTHING, related_name='categories')
    category = models.ForeignKey(to=Category, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, default=None)


class CourseOwners(models.Model):
    class Meta:
        db_table = 'course_owners'

    course = models.ForeignKey(to=Courses, on_delete=models.CASCADE, related_name='owners')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)


class CourseSections(models.Model):
    class Meta:
        db_table = 'course_sections'

    course = models.ForeignKey(to=Courses, on_delete=models.DO_NOTHING, related_name='sections')
    title = models.CharField(max_length=255)
    about_section = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, default=None)


class CourseSubSections(models.Model):
    class Meta:
        db_table = 'course_sub_sections'

    title = models.CharField(max_length=255)
    course_section = models.ForeignKey(to=CourseSections, on_delete=models.DO_NOTHING, related_name='sub_sections')
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, default=None)


class CourseSubSectionItems(models.Model):
    class Meta:
        db_table = 'course_sub_section_items'

    course_sub_section = models.ForeignKey(to=CourseSubSections, on_delete=models.DO_NOTHING,
                                           related_name='sub_section_item')
    title = models.CharField(max_length=255)
    type = models.ForeignKey(to=Enumerations, on_delete=models.DO_NOTHING)
    time_duration = models.IntegerField()
    price = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, default=None)


class CourseStatus(models.Model):
    class Meta:
        db_table = 'course_status'

    course = models.ForeignKey(to=Courses, on_delete=models.DO_NOTHING, related_name='statuses')
    status = models.ForeignKey(to=Enumerations, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, default=None)


# todo : this model must delete and setup in elastic as soon as possible
class CourseSubSectionItemContent(models.Model):
    class Meta:
        db_table = 'course_sub_section_item_contents'

    course_sub_section_item = models.ForeignKey(to=CourseSubSectionItems, on_delete=models.DO_NOTHING,
                                                related_name='sub_section_item_content')
    content = models.CharField(max_length=255, null=True, default=None)
    content_type = models.ForeignKey(to=Enumerations, on_delete=models.DO_NOTHING)
    file = models.ForeignKey(to=Files, on_delete=models.CASCADE, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, default=None)
