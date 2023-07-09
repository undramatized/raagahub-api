# raagahub-api
The Backend API for Raagahub Application, built on Django.

## Getting Started
[Reference Link](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-20-04)

### Setup Postgres Database
1. Ensure Postgres Server is running locally (Use Postgres.app)
2. Create database and admin user in psqlshell
```bash
postgres=# CREATE DATABASE raagahubdb;
postgres=# CREATE USER admin WITH PASSWORD 'admin123';
```
3. Grant necessary permissions
```bash
postgres=# ALTER ROLE admin SET client_encoding TO 'utf8';
postgres=# ALTER ROLE admin SET default_transaction_isolation TO 'read committed';
postgres=# ALTER ROLE admin SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE raagahubdb to admin;
```

### Run Virtual Environment
1. Create and activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
python -V # should indicate venv path as src
```
2. Install all python packages
```bash
pip install -r requirements.txt
```

### Perform migrations and dataload
1. Perform migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

2. Load Data in the following order
```bash
python manage.py loaddata chords
python manage.py loaddata melakarta_ragas
python manage.py loaddata janya_ragas
python manage.py loaddata krithis
```

### Run API server
```bash
python manage.py runserver
```

## Credits
The following sources have been crucial to building up this database:

https://en.wikipedia.org/wiki/Chord_names_and_symbols_(popular_music) 
https://spinditty.com/learning/chord-building-for-musicians 
http://www.carnatic.com/carnatic/ragalist.htm
