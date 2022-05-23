from django.db import models
from course.models import Courses
from accounts.models import User


class CourseLikes(models.Model):
    course = models.ForeignKey(to=Courses, on_delete=models.CASCADE, related_name='likes')
    action = models.BooleanField(default=True)
    liked_by = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='liked')
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        unique_together = ['course', 'liked_by']
        db_table = 'course_likes'


class CourseComments(models.Model):
    course = models.ForeignKey(to=Courses, on_delete=models.CASCADE, related_name='comments')
    commented_by = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    reply_to = models.ForeignKey(to='self', on_delete=models.DO_NOTHING, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        db_table = 'course_comments'


class CourseView(models.Model):
    course = models.ForeignKey(to=Courses, on_delete=models.CASCADE, related_name='view')
    viewed_by = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='views')
    created_at = models.DateTimeField(auto_now_add=True)
    meta_data = models.JSONField(null=True, default=None)

    class Meta:
        db_table = 'course_views'
