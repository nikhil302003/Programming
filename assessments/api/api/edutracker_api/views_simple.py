from rest_framework import viewsets, status, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count
from django.contrib.auth.models import User
from .models import Student, Course, Enrollment, Notification, CourseMaterial
from .serializers import (
    StudentSerializer, StudentCreateSerializer, StudentDashboardSerializer,
    CourseSerializer, CourseCreateSerializer,
    EnrollmentSerializer, EnrollmentCreateSerializer,
    NotificationSerializer,
    CourseMaterialSerializer, CourseMaterialCreateSerializer
)


class StudentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Student CRUD operations.
    """
    queryset = Student.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['student_id', 'first_name', 'last_name', 'email']
    ordering_fields = ['first_name', 'last_name', 'enrollment_date']
    ordering = ['last_name', 'first_name']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return StudentCreateSerializer
        elif self.action == 'dashboard':
            return StudentDashboardSerializer
        return StudentSerializer
    
    @action(detail=True, methods=['get'])
    def dashboard(self, request, pk=None):
        """Get student dashboard with enrolled courses and notifications."""
        student = self.get_object()
        serializer = self.get_serializer(student)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def enroll(self, request, pk=None):
        """Enroll student in a course."""
        student = self.get_object()
        course_id = request.data.get('course_id')
        
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if already enrolled
        if Enrollment.objects.filter(student=student, course=course).exists():
            return Response({'error': 'Already enrolled in this course'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check capacity
        if course.enrolled_count >= course.max_students:
            return Response({'error': 'Course is full'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create enrollment
        enrollment = Enrollment.objects.create(student=student, course=course)
        
        return Response(EnrollmentSerializer(enrollment).data, status=status.HTTP_201_CREATED)


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Course CRUD operations.
    """
    queryset = Course.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'course_code', 'instructor', 'description']
    ordering_fields = ['title', 'course_code', 'created_at']
    ordering = ['course_code']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CourseCreateSerializer
        return CourseSerializer
    
    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        """Get all students enrolled in this course."""
        course = self.get_object()
        enrollments = course.enrollments.filter(is_active=True)
        students = [enrollment.student for enrollment in enrollments]
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)


class EnrollmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Enrollment CRUD operations.
    """
    queryset = Enrollment.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['student__first_name', 'student__last_name', 'course__title']
    ordering_fields = ['enrollment_date', 'completion_percentage']
    ordering = ['-enrollment_date']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return EnrollmentCreateSerializer
        return EnrollmentSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Notification CRUD operations.
    """
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        # Filter notifications for the current user if they are a student
        user = self.request.user
        if hasattr(user, 'student_profile'):
            return Notification.objects.filter(recipient=user.student_profile)
        return Notification.objects.all()


class CourseMaterialViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Course Material CRUD operations.
    """
    queryset = CourseMaterial.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['order', 'created_at']
    ordering = ['course', 'order', 'created_at']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CourseMaterialCreateSerializer
        return CourseMaterialSerializer


class APIStatsView(APIView):
    """
    API endpoint to get platform statistics.
    """
    # permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        stats = {
            'total_students': Student.objects.filter(is_active=True).count(),
            'total_courses': Course.objects.filter(status='PUBLISHED').count(),
            'total_enrollments': Enrollment.objects.filter(is_active=True).count(),
            'completed_courses': Enrollment.objects.filter(status='COMPLETED').count(),
            'courses_by_level': dict(
                Course.objects.filter(status='PUBLISHED')
                .values('level')
                .annotate(count=Count('id'))
                .values_list('level', 'count')
            ),
            'recent_enrollments': Enrollment.objects.filter(
                is_active=True
            ).order_by('-enrollment_date')[:5].count(),
        }
        return Response(stats)
