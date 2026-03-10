from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_simple import (
    StudentViewSet, CourseViewSet, EnrollmentViewSet,
    NotificationViewSet, CourseMaterialViewSet, APIStatsView
)

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'materials', CourseMaterialViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('stats/', APIStatsView.as_view(), name='api-stats'),
]
