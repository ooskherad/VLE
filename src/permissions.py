from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    message = 'permission Denied, fuck you'

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id


class IsInstructor(permissions.BasePermission):
    def has_permission(self, request, view):
        from instructor.models import Instructor
        instructor = Instructor.objects.filter(user=request.user)
        return request.user.is_authenticated and instructor

    def has_object_permission(self, request, view, obj):
        from instructor.models import Instructor
        from course.models import CourseOwners
        if request.method in permissions.SAFE_METHODS:
            return True
        owner = CourseOwners.objects.get(obj.id)
        user = Instructor.objects.get(id=owner.instructor)
        return user.id == request.user.id
