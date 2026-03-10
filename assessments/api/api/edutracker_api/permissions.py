from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner of the object.
        return obj.user == request.user


class IsStudentOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow students or admin users to access.
    """
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            (hasattr(request.user, 'student_profile') or request.user.is_staff)
        )


class IsEnrolledStudent(permissions.BasePermission):
    """
    Custom permission to only allow enrolled students to access course materials.
    """
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        
        if hasattr(request.user, 'student_profile'):
            student = request.user.student_profile
            # Check if student is enrolled in the course
            if hasattr(obj, 'course'):
                return obj.course.enrollments.filter(student=student, is_active=True).exists()
            elif hasattr(obj, 'enrollments'):
                return obj.enrollments.filter(student=student, is_active=True).exists()
        
        return False
