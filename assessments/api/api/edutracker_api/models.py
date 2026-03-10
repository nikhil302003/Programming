from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.conf import settings
import os


class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=20, unique=True, help_text="Unique student identifier")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.TextField(blank=True, null=True)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    profile_picture = models.ImageField(upload_to='student_profiles/', blank=True, null=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = "Student"
        verbose_name_plural = "Students"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Course(models.Model):
    COURSE_LEVEL_CHOICES = [
        ('BEG', 'Beginner'),
        ('INT', 'Intermediate'),
        ('ADV', 'Advanced'),
    ]
    
    COURSE_STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('PUBLISHED', 'Published'),
        ('ARCHIVED', 'Archived'),
    ]
    
    title = models.CharField(max_length=200)
    course_code = models.CharField(max_length=20, unique=True, help_text="Unique course identifier")
    description = models.TextField()
    instructor = models.CharField(max_length=100)
    level = models.CharField(max_length=3, choices=COURSE_LEVEL_CHOICES, default='BEG')
    credits = models.PositiveIntegerField(default=3)
    duration_weeks = models.PositiveIntegerField(help_text="Course duration in weeks")
    max_students = models.PositiveIntegerField(default=50, help_text="Maximum number of students")
    status = models.CharField(max_length=10, choices=COURSE_STATUS_CHOICES, default='DRAFT')
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    video_file = models.FileField(
        upload_to='course_videos/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'mov', 'wmv'])],
        help_text="Upload course video (max 100MB)"
    )
    video_size = models.BigIntegerField(blank=True, null=True, help_text="Video file size in bytes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['course_code']
        verbose_name = "Course"
        verbose_name_plural = "Courses"
    
    def __str__(self):
        return f"{self.course_code}: {self.title}"
    
    @property
    def enrolled_count(self):
        return self.enrollments.filter(is_active=True).count()
    
    @property
    def available_slots(self):
        return self.max_students - self.enrolled_count
    
    def save(self, *args, **kwargs):
        if self.video_file:
            self.video_size = self.video_file.size
        super().save(*args, **kwargs)


class Enrollment(models.Model):
    ENROLLMENT_STATUS_CHOICES = [
        ('ENROLLED', 'Enrolled'),
        ('COMPLETED', 'Completed'),
        ('DROPPED', 'Dropped'),
        ('SUSPENDED', 'Suspended'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=ENROLLMENT_STATUS_CHOICES, default='ENROLLED')
    completion_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    grade = models.CharField(max_length=5, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['student', 'course']
        ordering = ['-enrollment_date']
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollments"
    
    def __str__(self):
        return f"{self.student.full_name} - {self.course.title}"


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('ENROLLMENT', 'New Enrollment'),
        ('COURSE_UPDATE', 'Course Updated'),
        ('GRADE', 'Grade Posted'),
        ('SYSTEM', 'System Notification'),
    ]
    
    recipient = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
    
    def __str__(self):
        return f"{self.title} - {self.recipient.full_name}"


class CourseMaterial(models.Model):
    MATERIAL_TYPES = [
        ('VIDEO', 'Video'),
        ('DOCUMENT', 'Document'),
        ('IMAGE', 'Image'),
        ('LINK', 'External Link'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    material_type = models.CharField(max_length=10, choices=MATERIAL_TYPES)
    file = models.FileField(
        upload_to='course_materials/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'ppt', 'pptx', 'jpg', 'jpeg', 'png', 'gif', 'mp4', 'avi', 'mov'])]
    )
    external_link = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Course Material"
        verbose_name_plural = "Course Materials"
    
    def __str__(self):
        return f"{self.title} - {self.course.title}"
