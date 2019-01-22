# Warsztaty - Django Advanced Module - Twitter Application
Application allows to send short messages (tweets) and comments beetwen users.

### Requirements
Program requires PostgreSQL database and Django.

### Installing
Create database 'twitter_db'. Install requirements  with command:
```
pip install -r requirements.txt
```
### Running the program
Apply the migrations:
```
python manage.py migrate
```
Start a development Web server on the local machine with command:
```
python manage.py runserver
```

### Usage Examples:
Add New Tweet:
```
http://127.0.0.1:8000/
```
List of Users:
```
http://127.0.0.1:8000/userslist/
```

