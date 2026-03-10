# EduTracker API Deployment & Testing Guide

## 🚀 Quick Setup Instructions

### 1. Install Python (if not already installed)
- Download Python 3.8+ from https://www.python.org/downloads/
- During installation, check "Add Python to PATH"
- Verify installation: `python --version`

### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Setup
```bash
# Copy .env file (if you have .env.example)
cp .env.example .env
# Edit .env file with your settings
```

### 5. Database Setup
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
# Follow prompts to create admin user
```

### 7. Run Development Server
```bash
python manage.py runserver
```

The server will start at: http://127.0.0.1:8000/

## 🧪 Testing the API

### 1. Access the API Root
Open your browser and go to:
```
http://127.0.0.1:8000/
```

You should see:
```json
{
    "message": "Welcome to EduTracker API",
    "endpoints": {
        "students": "/api/students/",
        "courses": "/api/courses/",
        "enrollments": "/api/enrollments/",
        "auth": "/api/auth/",
        "admin": "/admin/"
    }
}
```

### 2. Access Django Admin
Go to:
```
http://127.0.0.1:8000/admin/
```
Login with the superuser credentials you created.

### 3. Test API Endpoints with curl

#### Get Authentication Token
```bash
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your-username", "password": "your-password"}'
```

#### Create a Student
```bash
curl -X POST http://127.0.0.1:8000/api/students/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "STU001",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "date_of_birth": "2000-01-01",
    "gender": "M",
    "password": "securepassword123"
  }'
```

#### Create a Course
```bash
curl -X POST http://127.0.0.1:8000/api/courses/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Introduction to Python",
    "course_code": "PY101",
    "description": "Learn Python programming from scratch",
    "instructor": "Dr. Smith",
    "level": "BEG",
    "credits": 3,
    "duration_weeks": 8,
    "max_students": 50
  }'
```

#### Get All Students
```bash
curl -X GET http://127.0.0.1:8000/api/students/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

#### Get All Courses
```bash
curl -X GET http://127.0.0.1:8000/api/courses/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

#### Enroll Student in Course
```bash
curl -X POST http://127.0.0.1:8000/api/enrollments/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "student": 1,
    "course": 1
  }'
```

### 4. Test with Postman (Alternative)

1. **Import Collection**: Create a new collection in Postman
2. **Set Base URL**: `http://127.0.0.1:8000/api`
3. **Authentication**: 
   - Type: Bearer Token
   - Token: Your JWT token from `/api/auth/token/`

#### Sample Postman Requests:

**Get Token**
- Method: POST
- URL: `http://127.0.0.1:8000/api/auth/token/`
- Body (raw JSON):
```json
{
    "username": "your-username",
    "password": "your-password"
}
```

**Create Student**
- Method: POST
- URL: `http://127.0.0.1:8000/api/students/`
- Body (raw JSON):
```json
{
    "student_id": "STU002",
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "jane@example.com",
    "date_of_birth": "2000-02-01",
    "gender": "F",
    "password": "password123"
}
```

### 5. Test Real-time Notifications

You can test WebSocket connections using a simple HTML client:

Create `test_websocket.html`:
```html
<!DOCTYPE html>
<html>
<head>
    <title>WebSocket Test</title>
</head>
<body>
    <h1>WebSocket Notification Test</h1>
    <div id="messages"></div>
    
    <script>
        const ws = new WebSocket('ws://127.0.0.1:8000/ws/notifications/');
        
        ws.onopen = function(event) {
            console.log('WebSocket connected');
            document.getElementById('messages').innerHTML += '<p>Connected to WebSocket</p>';
        };
        
        ws.onmessage = function(event) {
            const data = JSON.parse(event.data);
            console.log('Received:', data);
            document.getElementById('messages').innerHTML += '<p>' + JSON.stringify(data) + '</p>';
        };
        
        ws.onclose = function(event) {
            console.log('WebSocket disconnected');
            document.getElementById('messages').innerHTML += '<p>Disconnected from WebSocket</p>';
        };
    </script>
</body>
</html>
```

Open this file in your browser after starting the Django server.

### 6. Run Tests
```bash
# Run all tests
python manage.py test

# Run specific test
python manage.py test edutracker_api.tests.StudentAPITest
```

## 🔧 Troubleshooting

### Common Issues:

1. **"python not found"**
   - Install Python from python.org
   - Check "Add Python to PATH" during installation

2. **ModuleNotFoundError**
   - Make sure virtual environment is activated
   - Run `pip install -r requirements.txt`

3. **Migration errors**
   - Delete `db.sqlite3` and run migrations again
   - Run `python manage.py makemigrations` then `python manage.py migrate`

4. **Permission errors**
   - Run terminal as administrator
   - Check folder permissions

### Port Issues:
If port 8000 is in use:
```bash
python manage.py runserver 8080
```

## 📱 API Documentation

### Authentication Endpoints:
- `POST /api/auth/token/` - Get JWT token
- `POST /api/auth/token/refresh/` - Refresh token

### Student Endpoints:
- `GET /api/students/` - List students
- `POST /api/students/` - Create student
- `GET /api/students/{id}/` - Get student
- `PUT /api/students/{id}/` - Update student
- `DELETE /api/students/{id}/` - Delete student
- `GET /api/students/{id}/dashboard/` - Student dashboard

### Course Endpoints:
- `GET /api/courses/` - List courses
- `POST /api/courses/` - Create course
- `GET /api/courses/{id}/` - Get course
- `PUT /api/courses/{id}/` - Update course
- `DELETE /api/courses/{id}/` - Delete course

### Enrollment Endpoints:
- `GET /api/enrollments/` - List enrollments
- `POST /api/enrollments/` - Create enrollment
- `GET /api/enrollments/{id}/` - Get enrollment
- `PUT /api/enrollments/{id}/` - Update enrollment

## 🚀 Production Deployment

### PythonAnywhere Deployment:
1. Upload project files
2. Create virtual environment
3. Install dependencies
4. Configure web app
5. Set up static files
6. Configure environment variables

See `pythonanywhere_setup.sh` for automated setup script.
