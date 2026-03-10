#!/bin/bash

# EduTracker PythonAnywhere Setup Script

echo "Setting up EduTracker API on PythonAnywhere..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating media directories..."
mkdir -p media/student_profiles
mkdir -p media/course_thumbnails
mkdir -p media/course_videos
mkdir -p media/course_materials
mkdir -p staticfiles

# Run migrations
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser (you'll need to do this manually)
echo "Setup complete!"
echo "Next steps:"
echo "1. Create a superuser: python manage.py createsuperuser"
echo "2. Configure your web app in PythonAnywhere dashboard"
echo "3. Set up environment variables"
echo "4. Configure static files serving"
echo "5. Set up worker for WebSocket support (if needed)"
