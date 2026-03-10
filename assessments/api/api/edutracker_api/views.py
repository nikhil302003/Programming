from rest_framework import viewsets, status, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
# from django_filters.rest_framework import DjangoFilterBackend
# from django_ratelimit.decorators import ratelimit
# from django.utils.decorators import method_decorator
from django.db.models import Count, Q
from django.contrib.auth.models import User
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
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
    # filterset_fields = ['gender', 'is_active']
    search_fields = ['student_id', 'first_name', 'last_name', 'email']
    ordering_fields = ['first_name', 'last_name', 'enrollment_date']
    ordering = ['last_name', 'first_name']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return StudentCreateSerializer
        elif self.action == 'dashboard':
            return StudentDashboardSerializer
        return StudentSerializer
    
    # @method_decorator(ratelimit(key='ip', rate='100/h', method='GET', block=True))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    # @method_decorator(ratelimit(key='ip', rate='50/h', method='POST', block=True))
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
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
        
        # Send real-time notification (disabled for now)
        # self._send_notification(
        #     student,
        #     'ENROLLMENT',
        #     'Successfully Enrolled',
        #     f'You have been successfully enrolled in {course.title}'
        # )
        
        return Response(EnrollmentSerializer(enrollment).data, status=status.HTTP_201_CREATED)
    
    def _send_notification(self, student, notification_type, title, message):
        """Helper method to send notifications."""
        notification = Notification.objects.create(
            recipient=student,
            title=title,
            message=message,
            notification_type=notification_type
        )
        
        # Send real-time notification via WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"student_{student.id}",
            {
                'type': 'notification_message',
                'notification': NotificationSerializer(notification).data
            }
        )


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Course CRUD operations.
    """
    queryset = Course.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['level', 'status']
    search_fields = ['title', 'course_code', 'instructor', 'description']
    ordering_fields = ['title', 'course_code', 'created_at']
    ordering = ['course_code']
    
    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return CourseCreateSerializer
        return CourseSerializer
    
    @method_decorator(ratelimit(key='ip', rate='200/h', method='GET', block=True))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @method_decorator(ratelimit(key='ip', rate='30/h', method='POST', block=True))
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        """Get all students enrolled in this course."""
        course = self.get_object()
        enrollments = course.enrollments.filter(is_active=True)
        students = [enrollment.student for enrollment in enrollments]
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """Publish the course."""
        course = self.get_object()
        course.status = 'PUBLISHED'
        course.save()
        
        # Notify all enrolled students
        for enrollment in course.enrollments.filter(is_active=True):
            self._send_notification(
                enrollment.student,
                'COURSE_UPDATE',
                'Course Published',
                f'The course "{course.title}" has been published.'
            )
        
        return Response({'status': 'Course published successfully'})
    
    def _send_notification(self, student, notification_type, title, message):
        """Helper method to send notifications."""
        notification = Notification.objects.create(
            recipient=student,
            title=title,
            message=message,
            notification_type=notification_type
        )
        
        # Send real-time notification via WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"student_{student.id}",
            {
                'type': 'notification_message',
                'notification': NotificationSerializer(notification).data
            }
        )


class EnrollmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Enrollment CRUD operations.
    """
    queryset = Enrollment.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'student', 'course']
    search_fields = ['student__first_name', 'student__last_name', 'course__title']
    ordering_fields = ['enrollment_date', 'completion_percentage']
    ordering = ['-enrollment_date']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return EnrollmentCreateSerializer
        return EnrollmentSerializer
    
    @method_decorator(ratelimit(key='ip', rate='150/h', method='GET', block=True))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'])
    def update_progress(self, request, pk=None):
        """Update student progress in course."""
        enrollment = self.get_object()
        completion_percentage = request.data.get('completion_percentage')
        
        if completion_percentage is not None:
            enrollment.completion_percentage = completion_percentage
            enrollment.save()
            
            # Send notification if course completed
            if completion_percentage >= 100 and enrollment.status != 'COMPLETED':
                enrollment.status = 'COMPLETED'
                enrollment.save()
                
                self._send_notification(
                    enrollment.student,
                    'GRADE',
                    'Course Completed',
                    f'Congratulations! You have completed {enrollment.course.title}'
                )
            
            return Response(EnrollmentSerializer(enrollment).data)
        
        return Response({'error': 'completion_percentage is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def drop(self, request, pk=None):
        """Drop student from course."""
        enrollment = self.get_object()
        enrollment.status = 'DROPPED'
        enrollment.is_active = False
        enrollment.save()
        
        self._send_notification(
            enrollment.student,
            'SYSTEM',
            'Course Dropped',
            f'You have been dropped from {enrollment.course.title}'
        )
        
        return Response({'status': 'Successfully dropped from course'})
    
    def _send_notification(self, student, notification_type, title, message):
        """Helper method to send notifications."""
        notification = Notification.objects.create(
            recipient=student,
            title=title,
            message=message,
            notification_type=notification_type
        )
        
        # Send real-time notification via WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"student_{student.id}",
            {
                'type': 'notification_message',
                'notification': NotificationSerializer(notification).data
            }
        )


class NotificationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Notification CRUD operations.
    """
    serializer_class = NotificationSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['notification_type', 'is_read', 'recipient']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        # Filter notifications for the current user if they are a student
        user = self.request.user
        if hasattr(user, 'student_profile'):
            return Notification.objects.filter(recipient=user.student_profile)
        return Notification.objects.all()
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark notification as read."""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'Notification marked as read'})
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read for the current user."""
        user = request.user
        if hasattr(user, 'student_profile'):
            notifications = Notification.objects.filter(recipient=user.student_profile, is_read=False)
            count = notifications.count()
            notifications.update(is_read=True)
            return Response({'status': f'{count} notifications marked as read'})
        return Response({'error': 'User is not a student'}, status=status.HTTP_400_BAD_REQUEST)


class CourseMaterialViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Course Material CRUD operations.
    """
    queryset = CourseMaterial.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['course', 'material_type', 'is_published']
    search_fields = ['title', 'description']
    ordering_fields = ['order', 'created_at']
    ordering = ['course', 'order', 'created_at']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CourseMaterialCreateSerializer
        return CourseMaterialSerializer
    
    @method_decorator(ratelimit(key='ip', rate='100/h', method='POST', block=True))
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class APIStatsView(APIView):
    """
    API endpoint to get platform statistics.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @method_decorator(ratelimit(key='ip', rate='50/h', method='GET', block=True))
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
