# WriteSphere - Blogging Platform

A modern Django-based blogging platform built for WriteHub Community, where users can write posts, interact with others, and follow their favorite authors.

## Features

### User Management
- User registration, login, logout with session handling
- Role-based access control (Admin, Author, Reader)
- User profiles with bio, avatar, and social links
- Follow/unfollow authors

### Blog Management
- Create, edit, delete blog posts
- Rich text content with cover images
- Categories and tags system
- Post status management (Draft, Published, Archived)
- Featured posts functionality
- Blog listing with filters (author, category, date range)

### Interaction Features
- Like/unlike system on blog posts
- Nested comments with replies
- 5-star rating system
- Follow/unfollow authors

### Admin Panel
- Customized Django admin interface
- Role-based access control
- Manage users, categories, posts, and comments
- Bulk actions for posts

### Technical Features
- MVT architecture with template inheritance
- Static and media file configuration
- MySQL database integration
- Responsive design with Bootstrap 5
- AJAX interactions for likes and comments
- Search functionality
- Pagination

## Tech Stack

- **Backend**: Django 6.0.3
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **JavaScript**: Vanilla JS with AJAX
- **Deployment**: PythonAnywhere ready

## Installation

### Prerequisites
- Python 3.8+
- MySQL 5.7+
- Virtual environment

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd writesphere
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv writesphere_env
   # Windows
   writesphere_env\Scripts\activate
   # Linux/Mac
   source writesphere_env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the project root:
   ```env
   DEBUG=True
   SECRET_KEY=your-secret-key-here-change-in-production
   DB_NAME=writesphere_db
   DB_USER=root
   DB_PASSWORD=your-mysql-password
   DB_HOST=localhost
   DB_PORT=3306
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Create MySQL database**
   ```sql
   CREATE DATABASE writesphere_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

6. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

9. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## Deployment on PythonAnywhere

### Prerequisites
- PythonAnywhere account
- MySQL database on PythonAnywhere

### Deployment Steps

1. **Upload your code**
   - Use Git or PythonAnywhere's file upload feature
   - Ensure all project files are uploaded

2. **Configure virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Set up database**
   - Create MySQL database on PythonAnywhere
   - Update database credentials in `.env` file

4. **Configure WSGI**
   - Update `wsgi.py` to use `pythonanywhere_settings`
   - Set the WSGI file path in PythonAnywhere dashboard

5. **Set environment variables**
   - Add all `.env` variables to PythonAnywhere's web app configuration

6. **Run migrations**
   ```bash
   python manage.py migrate
   ```

7. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Collect static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

9. **Configure web app**
   - Set the working directory
   - Set the virtual environment path
   - Set the WSGI file path
   - Reload the web app

## Project Structure

```
writesphere/
├── writesphere/          # Main Django project
│   ├── settings.py      # Development settings
│   ├── pythonanywhere_settings.py  # Production settings
│   ├── urls.py         # Main URL configuration
│   └── wsgi.py         # WSGI configuration
├── users/              # User management app
│   ├── models.py       # Custom User model
│   ├── views.py        # User views
│   ├── forms.py        # User forms
│   └── admin.py        # User admin
├── blog/               # Blog app
│   ├── models.py       # Post, Category, Tag models
│   ├── views.py        # Blog views
│   ├── forms.py        # Blog forms
│   └── admin.py        # Blog admin
├── interactions/       # Interactions app
│   ├── models.py       # Like, Comment, Follow models
│   ├── views.py        # Interaction views
│   └── admin.py        # Interaction admin
├── templates/          # HTML templates
│   ├── base.html       # Base template
│   ├── users/          # User templates
│   ├── blog/           # Blog templates
│   └── interactions/   # Interaction templates
├── static/             # Static files
│   ├── css/           # CSS files
│   ├── js/            # JavaScript files
│   └── images/        # Image files
├── media/              # Media files
│   ├── post_covers/   # Post cover images
│   └── profile_pics/  # Profile pictures
├── requirements.txt    # Python dependencies
├── .env               # Environment variables
└── README.md          # This file
```

## Usage

### For Users
1. Register for an account
2. Complete your profile
3. Start writing blog posts
4. Interact with other users' posts
5. Follow authors you like

### For Administrators
1. Access the admin panel at `/admin/`
2. Manage users, categories, and posts
3. Monitor user activity
4. Moderate content

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please contact the development team.

## Future Enhancements

- Email notifications
- Social media integration
- Advanced search with Elasticsearch
- REST API
- Mobile app
- Analytics dashboard
- Multi-language support
