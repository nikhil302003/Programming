from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Student, Course, Enrollment, Notification, CourseMaterial


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'first_name', 'last_name', 'email', 'enrollment_date', 'is_active']
    list_filter = ['gender', 'is_active', 'enrollment_date']
    search_fields = ['student_id', 'first_name', 'last_name', 'email']
    readonly_fields = ['enrollment_date']
    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'student_id', 'first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'gender')
        }),
        ('Address', {
            'fields': ('address',)
        }),
        ('Additional Information', {
            'fields': ('profile_picture', 'is_active', 'enrollment_date')
        }),
    )
    ordering = ['last_name', 'first_name']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_code', 'title', 'instructor', 'level', 'credits', 'enrolled_count', 'status']
    list_filter = ['level', 'status', 'created_at']
    search_fields = ['course_code', 'title', 'instructor']
    readonly_fields = ['created_at', 'updated_at', 'video_size', 'enrolled_count']
    fieldsets = (
        ('Basic Information', {
            'fields': ('course_code', 'title', 'description', 'instructor')
        }),
        ('Course Details', {
            'fields': ('level', 'credits', 'duration_weeks', 'max_students', 'status')
        }),
        ('Media', {
            'fields': ('thumbnail', 'video_file', 'video_size')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'enrolled_count')
        }),
    )
    ordering = ['course_code']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'enrollment_date', 'status', 'completion_percentage', 'grade']
    list_filter = ['status', 'enrollment_date']
    search_fields = ['student__first_name', 'student__last_name', 'course__title']
    readonly_fields = ['enrollment_date']
    fieldsets = (
        ('Enrollment Details', {
            'fields': ('student', 'course', 'enrollment_date', 'status')
        }),
        ('Progress', {
            'fields': ('completion_percentage', 'grade', 'is_active')
        }),
    )
    ordering = ['-enrollment_date']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'recipient', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['title', 'recipient__first_name', 'recipient__last_name']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Notification Details', {
            'fields': ('recipient', 'title', 'message', 'notification_type')
        }),
        ('Status', {
            'fields': ('is_read', 'created_at')
        }),
    )
    ordering = ['-created_at']


@admin.register(CourseMaterial)
class CourseMaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'material_type', 'order', 'is_published', 'created_at']
    list_filter = ['material_type', 'is_published', 'created_at']
    search_fields = ['title', 'course__title']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Material Details', {
            'fields': ('course', 'title', 'description', 'material_type')
        }),
        ('Content', {
            'fields': ('file', 'external_link')
        }),
        ('Settings', {
            'fields': ('order', 'is_published', 'created_at')
        }),
    )
    ordering = ['course', 'order', 'created_at']


# Customize User admin to show student information
class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False
    verbose_name_plural = 'Student Profile'


class CustomUserAdmin(UserAdmin):
    inlines = (StudentInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
