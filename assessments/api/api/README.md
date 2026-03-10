# EduTracker API

A comprehensive Django REST Framework API for managing students, courses, and enrollments in an EdTech platform.

## Features

### Core Functionality
- **Student Management**: CRUD operations for student profiles
- **Course Management**: Complete course management with video uploads
- **Enrollment System**: Student enrollment tracking and progress monitoring
- **Real-time Notifications**: WebSocket-based notifications
- **File Uploads**: Support for course videos and materials
- **Rate Limiting**: API protection against abuse
- **Token Authentication**: JWT-based authentication system

### Advanced Features
- **Real-time Notifications**: WebSocket integration for instant updates
- **Video Course Uploads**: File size validation and storage
- **Rate Limiting**: Configurable rate limits for API endpoints
- **Django Admin**: Comprehensive admin interface
- **API Statistics**: Platform analytics endpoint

## Tech Stack

- **Backend**: Django 4.2.7
- **API Framework**: Django REST Framework 3.14.0
- **Authentication**: JWT (Simple JWT)
- **Real-time**: Django Channels with Redis
- **Rate Limiting**: django-ratelimit
- **File Storage**: Django's built-in file system
- **Database**: SQLite (development), PostgreSQL (production)

## Installation

### Prerequisites
- Python 3.8+
- Redis server (for real-time notifications)
- Virtual environment

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd edutracker-api
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment Setup**
```bash
# Copy and edit the .env file
cp .env.example .env
# Update the .env file with your settings
```

5. **Database Setup**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create Superuser**
```bash
python manage.py createsuperuser
```

7. **Run the Server**
```bash
python manage.py runserver
```

## API Endpoints

### Authentication
- `POST /api/auth/token/` - Obtain JWT token
- `POST /api/auth/token/refresh/` - Refresh JWT token

### Students
- `GET /api/students/` - List all students
- `POST /api/students/` - Create new student
- `GET /api/students/{id}/` - Get student details
- `PUT /api/students/{id}/` - Update student
- `DELETE /api/students/{id}/` - Delete student
- `GET /api/students/{id}/dashboard/` - Student dashboard
- `POST /api/students/{id}/enroll/` - Enroll in course

### Courses
- `GET /api/courses/` - List all courses
- `POST /api/courses/` - Create new course
- `GET /api/courses/{id}/` - Get course details
- `PUT /api/courses/{id}/` - Update course
- `DELETE /api/courses/{id}/` - Delete course
- `GET /api/courses/{id}/students/` - Get enrolled students
- `POST /api/courses/{id}/publish/` - Publish course

### Enrollments
- `GET /api/enrollments/` - List all enrollments
- `POST /api/enrollments/` - Create enrollment
- `GET /api/enrollments/{id}/` - Get enrollment details
- `PUT /api/enrollments/{id}/` - Update enrollment
- `DELETE /api/enrollments/{id}/` - Delete enrollment
- `POST /api/enrollments/{id}/update_progress/` - Update progress
- `POST /api/enrollments/{id}/drop/` - Drop from course

### Notifications
- `GET /api/notifications/` - List notifications
- `POST /api/notifications/` - Create notification
- `GET /api/notifications/{id}/` - Get notification
- `POST /api/notifications/{id}/mark_read/` - Mark as read
- `POST /api/notifications/mark_all_read/` - Mark all as read

### Course Materials
- `GET /api/materials/` - List materials
- `POST /api/materials/` - Create material
- `GET /api/materials/{id}/` - Get material
- `PUT /api/materials/{id}/` - Update material
- `DELETE /api/materials/{id}/` - Delete material

### Statistics
- `GET /api/stats/` - Platform statistics

## WebSocket Endpoints

- `ws://localhost:8000/ws/notifications/` - Real-time notifications
- `ws://localhost:8000/ws/course-updates/` - Course updates

## Environment Variables

```bash
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440

# Redis Settings
REDIS_URL=redis://localhost:6379/0

# File Upload Settings
MAX_UPLOAD_SIZE=104857600  # 100MB

# Rate Limiting
RATE_LIMIT_ENABLE=True
RATE_LIMIT_RATE=100/h
```

## Rate Limiting

The API implements rate limiting to prevent abuse:

- **GET requests**: 100-200 requests per hour
- **POST requests**: 30-50 requests per hour
- **File uploads**: 100 requests per hour

Rate limits are configured per endpoint and can be adjusted in the `.env` file.

## File Uploads

### Supported Formats
- **Videos**: MP4, AVI, MOV, WMF
- **Documents**: PDF, DOC, DOCX, PPT, PPTX
- **Images**: JPG, JPEG, PNG, GIF

### File Size Limits
- **Course Videos**: Maximum 100MB
- **Course Materials**: Maximum 50MB

## Real-time Notifications

The system supports real-time notifications through WebSockets:

1. **Enrollment Notifications**: When a student enrolls in a course
2. **Course Updates**: When courses are published or updated
3. **Grade Notifications**: When grades are posted
4. **System Notifications**: General system updates

## Deployment

### PythonAnywhere Deployment

1. **Setup Virtual Environment**
```bash
virtualenv --python=python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Configure Web App**
- Set up a PythonAnywhere web app
- Point to your project directory
- Configure the WSGI file

3. **Database Setup**
- Set up PostgreSQL database
- Update settings with production database credentials

4. **Static Files**
- Configure static file serving
- Run `python manage.py collectstatic`

5. **Environment Variables**
- Set production environment variables in PythonAnywhere

### Security Considerations

- Set `DEBUG=False` in production
- Use a strong `SECRET_KEY`
- Configure `ALLOWED_HOSTS` properly
- Use HTTPS in production
- Set up proper CORS policies
- Configure Redis with authentication

## API Usage Examples

### Authentication
```bash
# Get token
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "student@example.com", "password": "password"}'

# Use token
curl -X GET http://localhost:8000/api/students/ \
  -H "Authorization: Bearer <your-token>"
```

### Create Student
```bash
curl -X POST http://localhost:8000/api/students/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "STU001",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "date_of_birth": "2000-01-01",
    "gender": "M",
    "password": "securepassword"
  }'
```

### Create Course
```bash
curl -X POST http://localhost:8000/api/courses/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Introduction to Python",
    "course_code": "PY101",
    "description": "Learn Python programming basics",
    "instructor": "Dr. Smith",
    "level": "BEG",
    "credits": 3,
    "duration_weeks": 8,
    "max_students": 50
  }'
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please open an issue on GitHub.
