# Greeter Guru
[![CircleCI](https://circleci.com/gh/VarenTechInternship/greeterguru.svg?style=svg)](https://circleci.com/gh/VarenTechInternship/greeterguru)

## Schematics

![Schematics](schematics.png)

## Installation

Execute first part of installation - make sure you're in the GreeterGuru directory
```bash
$ bin/install-1.sh
```
Manually create and enter virtual environment - after this, (cv) should always be displayed before username
```bash
$ source ~/.profile && mkvirtualenv cv -p python3
```
Execute second part of installation - there is a prompt at the beginning, and then you can leave it to finish executing, which will take around 60 minutes
```bash
$ bin/install-2.sh
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
