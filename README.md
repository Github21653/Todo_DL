
## Features

- Authentication: JWT-based authentication powered by rest_framework_simplejwt
- CORS Support: Configured for development environments with localhost access.
- Todo API: Full CRUD operations to manage tasks through a RESTful API.
- SQLite Database: The project uses SQLite as the default database for development and testing.
- Django Admin Panel: Allows easy management of users and tasks directly from the Django admin interface.




## Requirements

Before you begin, ensure that your environment meets the following requirements:
- Python: Version 3.8 or higher
- Django: Version 4.2.4 or higher
- Django Rest Framework: For API creation and management
- rest_framework_simplejwt: For JWT authentication
- corsheaders: To handle Cross-Origin Resource Sharing (CORS)


## Installation

Follow these steps to get the project up and running locally:

Clone the repository:
```bash
  https://github.com/Github21653/Todo_DL.git

  cd todo_dl
```

Apply the migrations to set up the database:
```bash
    python3 manage.py migrate
```

Create a superuser to access the Django admin panel: 
```bash
    python3 manage.py createsuperuser
```



