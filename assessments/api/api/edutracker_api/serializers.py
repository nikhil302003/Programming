from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Student, Course, Enrollment, Notification, CourseMaterial


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    full_name = serializers.ReadOnlyField()
    enrolled_courses = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = [
            'id', 'user', 'student_id', 'first_name', 'last_name', 'email',
            'phone', 'date_of_birth', 'gender', 'address', 'enrollment_date',
            'is_active', 'profile_picture', 'full_name', 'enrolled_courses'
        ]
        read_only_fields = ['id', 'enrollment_date', 'full_name']
    
    def get_enrolled_courses(self, obj):
        enrollments = obj.enrollments.filter(is_active=True, status='ENROLLED')
        return EnrollmentSerializer(enrollments, many=True).data


class StudentCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = Student
        fields = [
            'student_id', 'first_name', 'last_name', 'email', 'phone',
            'date_of_birth', 'gender', 'address', 'password', 'user'
        ]
    
    def create(self, validated_data):
        user_data = validated_data.pop('user', None)
        password = validated_data.pop('password')
        
        # Create User account
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=password
        )
        
        # Create Student profile
        student = Student.objects.create(user=user, **validated_data)
        return student


class CourseSerializer(serializers.ModelSerializer):
    enrolled_count = serializers.ReadOnlyField()
    available_slots = serializers.ReadOnlyField()
    materials = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'course_code', 'description', 'instructor', 'level',
            'credits', 'duration_weeks', 'max_students', 'status', 'thumbnail',
            'video_file', 'video_size', 'created_at', 'updated_at',
            'enrolled_count', 'available_slots', 'materials'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'enrolled_count', 'available_slots']
    
    def get_materials(self, obj):
        materials = obj.materials.filter(is_published=True)
        return CourseMaterialSerializer(materials, many=True).data


class CourseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'title', 'course_code', 'description', 'instructor', 'level',
            'credits', 'duration_weeks', 'max_students', 'status', 'thumbnail',
            'video_file'
        ]
    
    def validate_video_file(self, value):
        if value:
            max_size = 100 * 1024 * 1024  # 100MB
            if value.size > max_size:
                raise serializers.ValidationError("Video file size cannot exceed 100MB.")
        return value


class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    course_code = serializers.CharField(source='course.course_code', read_only=True)
    
    class Meta:
        model = Enrollment
        fields = [
            'id', 'student', 'course', 'enrollment_date', 'status',
            'completion_percentage', 'grade', 'is_active', 'student_name',
            'course_title', 'course_code'
        ]
        read_only_fields = ['id', 'enrollment_date']


class EnrollmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['student', 'course']
    
    def validate(self, data):
        student = data['student']
        course = data['course']
        
        # Check if student is already enrolled
        if Enrollment.objects.filter(student=student, course=course).exists():
            raise serializers.ValidationError("Student is already enrolled in this course.")
        
        # Check if course has available slots
        if course.enrolled_count >= course.max_students:
            raise serializers.ValidationError("Course has reached maximum capacity.")
        
        return data


class NotificationSerializer(serializers.ModelSerializer):
    recipient_name = serializers.CharField(source='recipient.full_name', read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'title', 'message', 'notification_type',
            'is_read', 'created_at', 'recipient_name'
        ]
        read_only_fields = ['id', 'created_at']


class CourseMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseMaterial
        fields = [
            'id', 'course', 'title', 'description', 'material_type',
            'file', 'external_link', 'order', 'is_published', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class CourseMaterialCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseMaterial
        fields = [
            'course', 'title', 'description', 'material_type',
            'file', 'external_link', 'order', 'is_published'
        ]
    
    def validate(self, data):
        material_type = data.get('material_type')
        file = data.get('file')
        external_link = data.get('external_link')
        
        if material_type in ['VIDEO', 'DOCUMENT', 'IMAGE'] and not file:
            raise serializers.ValidationError(f"File is required for {material_type} materials.")
        
        if material_type == 'LINK' and not external_link:
            raise serializers.ValidationError("External link is required for LINK materials.")
        
        return data


class StudentDashboardSerializer(serializers.ModelSerializer):
    enrolled_courses = serializers.SerializerMethodField()
    completed_courses = serializers.SerializerMethodField()
    notifications = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = [
            'id', 'student_id', 'first_name', 'last_name', 'email',
            'enrolled_courses', 'completed_courses', 'notifications'
        ]
    
    def get_enrolled_courses(self, obj):
        enrollments = obj.enrollments.filter(is_active=True, status='ENROLLED')
        return EnrollmentSerializer(enrollments, many=True).data
    
    def get_completed_courses(self, obj):
        enrollments = obj.enrollments.filter(status='COMPLETED')
        return EnrollmentSerializer(enrollments, many=True).data
    
    def get_notifications(self, obj):
        notifications = obj.notifications.filter(is_read=False)[:5]
        return NotificationSerializer(notifications, many=True).data
