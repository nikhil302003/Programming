# 🚀 Quick Start Guide

## Step 1: Install Python
1. Go to https://www.python.org/downloads/
2. Download Python 3.8+ 
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Verify: Open Command Prompt and run `python --version`

## Step 2: Setup Project
```bash
# Navigate to project directory
cd c:/Users/dell/OneDrive/Desktop/api

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Setup Database
```bash
# Create database tables
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
```

## Step 4: Run Server
```bash
python manage.py runserver
```

## Step 5: Test API
1. Open browser: http://127.0.0.1:8000/
2. Go to admin: http://127.0.0.1:8000/admin/
3. Test API endpoints using Postman or curl

## 🎯 Quick Test Commands

### Get API Info
```bash
curl http://127.0.0.1:8000/
```

### Create Student (after getting token)
```bash
curl -X POST http://127.0.0.1:8000/api/students/ \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "TEST001",
    "first_name": "Test",
    "last_name": "User",
    "email": "test@example.com",
    "date_of_birth": "2000-01-01",
    "gender": "M",
    "password": "password123"
  }'
```

## 🔧 If You Get Errors

### "python not found"
- Reinstall Python with "Add to PATH" checked
- Or use full path: `C:\Python312\python.exe`

### "ModuleNotFoundError"
- Make sure virtual environment is active
- Run: `pip install -r requirements.txt`

### Port 8000 in use
- Use different port: `python manage.py runserver 8080`

## 📱 Testing Tools

1. **Browser**: http://127.0.0.1:8000/
2. **Admin Panel**: http://127.0.0.1:8000/admin/
3. **Postman**: Import API endpoints
4. **WebSocket Test**: Open `test_websocket.html`

## 🎉 Success Indicators

✅ Server starts without errors  
✅ API root page loads in browser  
✅ Admin panel accessible  
✅ Can create students/courses  
✅ Real-time notifications work  

## 📞 Need Help?

Check the full `DEPLOYMENT_GUIDE.md` for detailed instructions and troubleshooting.
