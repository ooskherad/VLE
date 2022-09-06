from django.db import models
from django.contrib.auth import get_user_model

from course.models import Courses, CourseSubSections
from home.models import Enumerations


class Enrollments(models.Model):
    class Meta:
        db_table = 'enrollments'

    course = models.ForeignKey(to=Courses, on_delete=models.CASCADE, related_name='course_enrolls')
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name='user_enrolls')
    status = models.ForeignKey(to=Enumerations, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, default=None)


class EnrollmentStatus(models.Model):
    class Meta:
        db_table = 'enrollment_status'

    enroll = models.ForeignKey(to=Enrollments, on_delete=models.DO_NOTHING, related_name='statuses')
    status = models.ForeignKey(to=Enumerations, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, default=None)


class CourseItemEnrollmentStatus(models.Model):
    class Meta:
        db_table = 'course_item_enrollment_status'

    enroll = models.ForeignKey(to=Enrollments, on_delete=models.DO_NOTHING, related_name='item_statuses')
    course_item = models.ForeignKey(to=CourseSubSections, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, default=None)
