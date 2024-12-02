Hello
**Django Todo Application**
This is a simple Todo application built using Django, Django Rest Framework, and SQLite as the database. It includes JWT authentication for secure user access and supports Cross-Origin Resource Sharing (CORS) for development purposes.

**Features**
Authentication: JWT-based authentication using rest_framework_simplejwt.
CORS: Supports CORS for development with localhost.
Todo API: A basic API for managing tasks (CRUD operations).
SQLite Database: Default database used for development and testing.
Admin Panel: Django admin interface for managing users and tasks.

**Requirements**
Python 3.8 or higher
Django 4.2.4 or higher
Django Rest Framework
djangorestframework_simplejwt for JWT authentication
corsheaders for CORS support

Running the Project
Apply the migrations:  python3 manage.py migrate
Create a superuser to access the Django admin panel:  python manage.py createsuperuser
Run the development server:  python manage.py runserver


**Project Structure**
todo_dl/
├── api/                        # Application for managing API logic
│   ├── migrations/              # Database migrations
│   ├── models.py                # Django models for tasks and users
│   ├── views.py                 # API views
│   └── urls.py                  # URL routing for API endpoints
├── todo_dl/                     # Main project folder
│   ├── settings.py              # Project settings
│   ├── urls.py                  # Main URL routing
│   ├── wsgi.py                  # WSGI configuration
│   └── asgi.py                  # ASGI configuration
├── manage.py                    # Django management commands
└── requirements.txt             # Project dependencies

