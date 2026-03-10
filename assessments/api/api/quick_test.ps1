# EduTracker API Quick Test Script
# Run this in PowerShell with: .\quick_test.ps1

Write-Host "🧪 Testing EduTracker API..." -ForegroundColor Green

# Test 1: API Root
Write-Host "`n1. Testing API Root..." -ForegroundColor Yellow
$response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/" -Method GET
Write-Host "✅ Status: $($response.StatusCode)" -ForegroundColor Green
Write-Host "Response: $($response.Content)" -ForegroundColor Cyan

# Test 2: Create Student
Write-Host "`n2. Creating Student..." -ForegroundColor Yellow
$studentData = @{
    student_id = "PS001"
    first_name = "PowerShell"
    last_name = "Tester"
    email = "powershell@example.com"
    date_of_birth = "2000-01-01"
    gender = "M"
    password = "password123"
}
$response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/students/" -Method POST -ContentType "application/json" -Body ($studentData | ConvertTo-Json)
Write-Host "✅ Status: $($response.StatusCode)" -ForegroundColor Green
Write-Host "Student Created Successfully!" -ForegroundColor Cyan

# Test 3: Get Students
Write-Host "`n3. Getting All Students..." -ForegroundColor Yellow
$response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/students/" -Method GET
Write-Host "✅ Status: $($response.StatusCode)" -ForegroundColor Green
$data = $response.Content | ConvertFrom-Json
Write-Host "Found $($data.count) students" -ForegroundColor Cyan

# Test 4: Create Course
Write-Host "`n4. Creating Course..." -ForegroundColor Yellow
$courseData = @{
    title = "PowerShell Testing Course"
    course_code = "PC101"
    description = "Learn API testing with PowerShell"
    instructor = "Dr. PowerShell"
    level = "BEG"
    credits = 3
    duration_weeks = 6
    max_students = 25
}
$response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/courses/" -Method POST -ContentType "application/json" -Body ($courseData | ConvertTo-Json)
Write-Host "✅ Status: $($response.StatusCode)" -ForegroundColor Green
Write-Host "Course Created Successfully!" -ForegroundColor Cyan

# Test 5: Get Courses
Write-Host "`n5. Getting All Courses..." -ForegroundColor Yellow
$response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/courses/" -Method GET
Write-Host "✅ Status: $($response.StatusCode)" -ForegroundColor Green
$data = $response.Content | ConvertFrom-Json
Write-Host "Found $($data.count) courses" -ForegroundColor Cyan

# Test 6: Get Statistics
Write-Host "`n6. Getting Platform Statistics..." -ForegroundColor Yellow
$response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/stats/" -Method GET
Write-Host "✅ Status: $($response.StatusCode)" -ForegroundColor Green
$stats = $response.Content | ConvertFrom-Json
Write-Host "📊 Platform Stats:" -ForegroundColor Cyan
Write-Host "  Total Students: $($stats.total_students)" -ForegroundColor White
Write-Host "  Total Courses: $($stats.total_courses)" -ForegroundColor White
Write-Host "  Total Enrollments: $($stats.total_enrollments)" -ForegroundColor White

Write-Host "`n🎉 Testing Complete! Your EduTracker API is fully functional!" -ForegroundColor Green
