### BOOKSAPP
This is a simple project built with django and django-rest-framework.
It exposes apis for:
- user login
- user sign up
- password resets
- create books
- fetch books

### set up
- clone this repository
- create a `.env` file with the following content
```

DB_ENGINE='django.db.backends.mysql' 
DB_HOST='your_db_host'
DB_NAME='your_db_name'
DB_USER='your_db_user'
DB_PASSWORD='your_db_password'

EMAIL_HOST=''
EMAIL_HOST_USER=''
EMAIL_HOST_PASSWORD=''
EMAIL_PORT=''
```
- run the migrations with the following command `python3 manage.py migrate`.
