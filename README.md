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
$ python3 manage.py makemigrations
$ python3 manage.py migrate --run-syncdb
```

#During first login / Create Superuser:
```bash
$ python3 manage.py makemigrations
$ python3 manage.py createsuperuser
```
## If needed, flush database & reset migrations
```bash
$ cd GGProject
$ python3 manage.py flush #flushes database
$ find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
$ find . -path "*/migrations/*.pyc" -delete
$ python3 manage.py makemigrations
$ python3 manage.py createsuperuser
$ python3 manage.py migrate --run-syncdb
$ python3 manage.py runserver
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