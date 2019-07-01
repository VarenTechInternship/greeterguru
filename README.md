# Greeter Guru
[![CircleCI](https://circleci.com/gh/VarenTechInternship/greeterguru.svg?style=svg)](https://circleci.com/gh/VarenTechInternship/greeterguru)
## Schematics

![Schematics](schematics.png)

## Installation

Create a virtual environment:
```bash
$ python3 -m venv env
```

Start your virtual environment by running:
```bash
$ source env/bin/activate
```
Installing packages with requirements
```bash
$ pip3 install -r requirements.txt
```

## Running the Application
```bash
$ cd GGProject
$ python3 manage.py makemigrations #Create Database Tables
$ python3 manage.py migrate --run-syncdb #Create New Migration File and Inserts Model Data into Database
$ python3 manage.py runserver #Run Server
```
--> During First Login / Migration Create Superuser:
```bash
$ python3 manage.py makemigrations
$ python3 manage.py createsuperuser #Create Login Root User
```
## If Needed, Flush Database and Reset Migrations
```bash
$ cd GGProject
$ python3 manage.py flush #Flush Database
$ find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
$ find . -path "*/migrations/*.pyc"  -delete #Delete all Files in Migrations Folder except __init__.py
$ python3 manage.py makemigrations #Create Tables
$ python3 manage.py createsuperuser #Create Admin User
$ python3 manage.py migrate --run-syncdb #Migrate and Put Model Information in Database
$ python3 manage.py runserver #Run Server

```

## Directories Overview

**FaceID:** Face detection and recognition package. Implements bulk of project's functionality.

--> **Datset:** Pictures of each employee.

--> **Cascade:** Reference file for face detection.

--> **Trainer:** Results from training the model.

**GGProject:** Root directory of GreeterGuru Django project.

--> **GreeterGuru:** Django project package.

--> **workflow:** Django application. Handles project workflow.

--> **api:** Django application. Implements necessary APIs.

--> **scripts:** Additional python scripts for Django project.

**.circleci:** CircleCI directory. Used to automate testing.

**venv:** Virtual environment.
