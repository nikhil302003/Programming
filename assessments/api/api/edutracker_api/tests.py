from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Student, Course, Enrollment, Notification


class StudentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.student = Student.objects.create(
            user=self.user,
            student_id='STU001',
            first_name='John',
            last_name='Doe',
            email='test@example.com',
            date_of_birth='2000-01-01',
            gender='M'
        )

    def test_student_creation(self):
        self.assertEqual(self.student.full_name, 'John Doe')
        self.assertEqual(str(self.student), 'John Doe (STU001)')

    def test_student_enrollment_count(self):
        course = Course.objects.create(
            title='Test Course',
            course_code='TC101',
            description='Test Description',
            instructor='Test Instructor'
        )
        Enrollment.objects.create(student=self.student, course=course)
        self.assertEqual(self.student.enrollments.count(), 1)


class CourseModelTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title='Python Programming',
            course_code='PY101',
            description='Learn Python',
            instructor='Dr. Smith',
            max_students=30
        )

    def test_course_creation(self):
        self.assertEqual(str(self.course), 'PY101: Python Programming')
        self.assertEqual(self.course.enrolled_count, 0)
        self.assertEqual(self.course.available_slots, 30)

    def test_course_capacity(self):
        user = User.objects.create_user(
            username='student1',
            email='student1@example.com',
            password='pass123'
        )
        student = Student.objects.create(
            user=user,
            student_id='STU001',
            first_name='Jane',
            last_name='Doe',
            email='student1@example.com',
            date_of_birth='2000-01-01',
            gender='F'
        )
        Enrollment.objects.create(student=student, course=self.course)
        self.assertEqual(self.course.enrolled_count, 1)
        self.assertEqual(self.course.available_slots, 29)


class StudentAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.student = Student.objects.create(
            user=self.user,
            student_id='STU001',
            first_name='John',
            last_name='Doe',
            email='test@example.com',
            date_of_birth='2000-01-01',
            gender='M'
        )

    def test_get_students_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/students/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_student(self):
        data = {
            'student_id': 'STU002',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane@example.com',
            'date_of_birth': '2000-02-01',
            'gender': 'F',
            'password': 'newpass123'
        }
        response = self.client.post('/api/students/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 2)


class CourseAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123',
            is_staff=True
        )
        self.course = Course.objects.create(
            title='Test Course',
            course_code='TC101',
            description='Test Description',
            instructor='Test Instructor'
        )

    def test_get_courses_list(self):
        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_course(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Course',
            'course_code': 'NC101',
            'description': 'New Description',
            'instructor': 'New Instructor',
            'level': 'BEG',
            'credits': 3,
            'duration_weeks': 8,
            'max_students': 50
        }
        response = self.client.post('/api/courses/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)


class EnrollmentAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.student = Student.objects.create(
            user=self.user,
            student_id='STU001',
            first_name='John',
            last_name='Doe',
            email='test@example.com',
            date_of_birth='2000-01-01',
            gender='M'
        )
        self.course = Course.objects.create(
            title='Test Course',
            course_code='TC101',
            description='Test Description',
            instructor='Test Instructor'
        )

    def test_create_enrollment(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'student': self.student.id,
            'course': self.course.id
        }
        response = self.client.post('/api/enrollments/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Enrollment.objects.count(), 1)

    def test_duplicate_enrollment(self):
        # Create first enrollment
        Enrollment.objects.create(student=self.student, course=self.course)
        
        self.client.force_authenticate(user=self.user)
        data = {
            'student': self.student.id,
            'course': self.course.id
        }
        response = self.client.post('/api/enrollments/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class NotificationAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.student = Student.objects.create(
            user=self.user,
            student_id='STU001',
            first_name='John',
            last_name='Doe',
            email='test@example.com',
            date_of_birth='2000-01-01',
            gender='M'
        )
        self.notification = Notification.objects.create(
            recipient=self.student,
            title='Test Notification',
            message='Test message',
            notification_type='SYSTEM'
        )

    def test_get_notifications_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/notifications/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_mark_notification_read(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f'/api/notifications/{self.notification.id}/mark_read/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)
