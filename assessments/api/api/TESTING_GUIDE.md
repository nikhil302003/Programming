# 🧪 EduTracker API Testing Guide

## 🚀 Quick Testing Methods

### Method 1: Browser Testing (Easiest)

1. **Open your browser and go to:**
   - **API Root**: http://127.0.0.1:8000/
   - **Admin Panel**: http://127.0.0.1:8000/admin/
   - **Students API**: http://127.0.0.1:8000/api/students/
   - **Courses API**: http://127.0.0.1:8000/api/courses/

2. **Admin Panel Login:**
   - Username: `admin`
   - Password: (leave blank for now)

### Method 2: PowerShell Commands (Windows)

```powershell
# Test API Root
Invoke-WebRequest -Uri "http://127.0.0.1:8000/" -Method GET

# Create a Student
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/students/" -Method POST -ContentType "application/json" -Body '{
    "student_id": "TEST001",
    "first_name": "Test",
    "last_name": "User",
    "email": "test@example.com",
    "date_of_birth": "2000-01-01",
    "gender": "M",
    "password": "password123"
}'

# Get All Students
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/students/" -Method GET

# Create a Course
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/courses/" -Method POST -ContentType "application/json" -Body '{
    "title": "Test Course",
    "course_code": "TC101",
    "description": "This is a test course",
    "instructor": "Test Instructor",
    "level": "BEG",
    "credits": 3,
    "duration_weeks": 8,
    "max_students": 50
}'

# Get All Courses
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/courses/" -Method GET

# Create Enrollment
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/enrollments/" -Method POST -ContentType "application/json" -Body '{
    "student": 1,
    "course": 1
}'

# Get Platform Statistics
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/stats/" -Method GET
```

### Method 3: curl Commands (Cross-platform)

```bash
# Test API Root
curl http://127.0.0.1:8000/

# Create Student
curl -X POST http://127.0.0.1:8000/api/students/ \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "CURL001",
    "first_name": "Curl",
    "last_name": "User",
    "email": "curl@example.com",
    "date_of_birth": "2000-01-01",
    "gender": "M",
    "password": "password123"
  }'

# Get Students
curl http://127.0.0.1:8000/api/students/

# Create Course
curl -X POST http://127.0.0.1:8000/api/courses/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Curl Course",
    "course_code": "CC101",
    "description": "Testing with curl",
    "instructor": "Dr. Curl",
    "level": "BEG",
    "credits": 3,
    "duration_weeks": 8,
    "max_students": 30
  }'

# Get Courses
curl http://127.0.0.1:8000/api/courses/

# Get Stats
curl http://127.0.0.1:8000/api/stats/
```

### Method 4: Python Script

Create a test file `test_api.py`:

```python
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_api():
    print("🧪 Testing EduTracker API...")
    
    # Test 1: Get API Root
    print("\n1. Testing API Root...")
    response = requests.get("http://127.0.0.1:8000/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 2: Create Student
    print("\n2. Creating Student...")
    student_data = {
        "student_id": "PY001",
        "first_name": "Python",
        "last_name": "Tester",
        "email": "python@example.com",
        "date_of_birth": "2000-01-01",
        "gender": "M",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/students/", json=student_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 3: Get Students
    print("\n3. Getting All Students...")
    response = requests.get(f"{BASE_URL}/students/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 4: Create Course
    print("\n4. Creating Course...")
    course_data = {
        "title": "Python Testing Course",
        "course_code": "PT101",
        "description": "Learn how to test APIs",
        "instructor": "Dr. Test",
        "level": "BEG",
        "credits": 3,
        "duration_weeks": 6,
        "max_students": 25
    }
    response = requests.post(f"{BASE_URL}/courses/", json=course_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 5: Get Courses
    print("\n5. Getting All Courses...")
    response = requests.get(f"{BASE_URL}/courses/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 6: Create Enrollment
    print("\n6. Creating Enrollment...")
    enrollment_data = {
        "student": 1,
        "course": 1
    }
    response = requests.post(f"{BASE_URL}/enrollments/", json=enrollment_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 7: Get Stats
    print("\n7. Getting Platform Statistics...")
    response = requests.get(f"{BASE_URL}/stats/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    print("\n✅ Testing Complete!")

if __name__ == "__main__":
    test_api()
```

Run it with: `python test_api.py`

### Method 5: Postman (GUI Testing)

1. **Download Postman** from https://www.postman.com/
2. **Create New Collection**: "EduTracker API"
3. **Add Requests**:

#### **Student Endpoints:**
- **GET Students**: 
  - Method: GET
  - URL: `http://127.0.0.1:8000/api/students/`
  
- **POST Student**:
  - Method: POST
  - URL: `http://127.0.0.1:8000/api/students/`
  - Body → raw → JSON:
  ```json
  {
    "student_id": "POST001",
    "first_name": "Postman",
    "last_name": "User",
    "email": "postman@example.com",
    "date_of_birth": "2000-01-01",
    "gender": "M",
    "password": "password123"
  }
  ```

#### **Course Endpoints:**
- **GET Courses**:
  - Method: GET
  - URL: `http://127.0.0.1:8000/api/courses/`
  
- **POST Course**:
  - Method: POST
  - URL: `http://127.0.0.1:8000/api/courses/`
  - Body → raw → JSON:
  ```json
  {
    "title": "Postman Testing Course",
    "course_code": "PC101",
    "description": "Testing with Postman",
    "instructor": "Dr. Postman",
    "level": "BEG",
    "credits": 3,
    "duration_weeks": 8,
    "max_students": 30
  }
  ```

### Method 6: Web Browser Direct API Testing

You can also test directly in your browser's address bar for GET requests:

- http://127.0.0.1:8000/
- http://127.0.0.1:8000/api/students/
- http://127.0.0.1:8000/api/courses/
- http://127.0.0.1:8000/api/enrollments/
- http://127.0.0.1:8000/api/stats/

## 🔍 Advanced Testing

### Test Specific Student Dashboard
```powershell
# Get student dashboard (replace 1 with actual student ID)
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/students/1/dashboard/" -Method GET
```

### Test Course Students
```powershell
# Get students enrolled in a course (replace 1 with actual course ID)
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/courses/1/students/" -Method GET
```

### Test Search and Filtering
```powershell
# Search students by name
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/students/?search=John" -Method GET

# Search courses by title
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/courses/?search=Python" -Method GET
```

## 📊 Expected Results

### Successful Student Creation Response:
```json
{
  "student_id": "TEST001",
  "first_name": "Test",
  "last_name": "User",
  "email": "test@example.com",
  "phone": null,
  "date_of_birth": "2000-01-01",
  "gender": "M",
  "address": null,
  "user": {
    "id": 2,
    "username": "test@example.com",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User"
  },
  "enrollment_date": "2026-03-04T10:40:00.000Z",
  "is_active": true,
  "profile_picture": null,
  "full_name": "Test User",
  "enrolled_courses": []
}
```

### Successful Course Creation Response:
```json
{
  "title": "Test Course",
  "course_code": "TC101",
  "description": "This is a test course",
  "instructor": "Test Instructor",
  "level": "BEG",
  "credits": 3,
  "duration_weeks": 8,
  "max_students": 50,
  "status": "DRAFT",
  "thumbnail": null,
  "video_file": null,
  "video_size": null,
  "created_at": "2026-03-04T10:40:00.000Z",
  "updated_at": "2026-03-04T10:40:00.000Z",
  "enrolled_count": 0,
  "available_slots": 50,
  "materials": []
}
```

### Platform Statistics Response:
```json
{
  "total_students": 1,
  "total_courses": 1,
  "total_enrollments": 1,
  "completed_courses": 0,
  "courses_by_level": {
    "BEG": 1
  },
  "recent_enrollments": 1
}
```

## 🚨 Troubleshooting

### Common Issues:

1. **"Authentication credentials were not provided"**
   - This is expected for POST/PUT/DELETE requests
   - Authentication is temporarily disabled for testing

2. **"Server not responding"**
   - Make sure the Django server is running
   - Check: http://127.0.0.1:8000/ is accessible

3. **"JSON parse error"**
   - Check your JSON syntax
   - Use proper quotes and commas

4. **"Method not allowed"**
   - Make sure you're using the correct HTTP method
   - GET for retrieval, POST for creation

5. **"404 Not Found"**
   - Check the URL is correct
   - Make sure server is running on port 8000

## 🎯 Quick Test Checklist

- [ ] Server running on http://127.0.0.1:8000/
- [ ] API root returns welcome message
- [ ] Can create a student
- [ ] Can list all students
- [ ] Can create a course
- [ ] Can list all courses
- [ ] Can create an enrollment
- [ ] Can get platform statistics
- [ ] Admin panel accessible

## 📱 Mobile Testing

You can also test from your mobile device (if on same network):

1. Find your computer's IP address: `ipconfig`
2. Replace `127.0.0.1` with your IP address
3. Access from mobile: `http://YOUR_IP:8000/`

**Happy Testing! 🎉**
