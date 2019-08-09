# Greeter Guru
[![CircleCI](https://circleci.com/gh/VarenTechInternship/greeterguru.svg?style=svg)](https://circleci.com/gh/VarenTechInternship/greeterguru)

## Schematics

![Schematics](schematics.png)

## Installation

Execute first part of installation - make sure that you're in the GreeterGuru directory
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
Set up Active Directory and Web Server automatically
```bash
$ bin/setup.sh
```
NOTE: To uninstall OpenCV and the virtual environment run the following command - this may be necessary if the installation process fails partway through
```bash
$ bin/uninstall.sh
```

## Manually set up Active Directory and Server
Create A Secure LDAPS Connection
```bash
$ sudo su   # Switch user to root
$ sed -i '/TLS_REQCERT never/d' /etc/ldap/ldap.conf # Remove - if exists - secure connection
$ echo "TLS_REQCERT never" >> /etc/ldap/ldap.conf # Create secure connection via ldap
```
Run the Application
```bash
$ cd GGProject
$ python3 manage.py makemigrations
$ python3 manage.py migrate --run-syncdb
```
Create Superuser:
```bash
$ python3 manage.py createsuperuser
```

## Troubleshooting manual connections
To remove all users, flush database & reset migrations
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
For password hash issues, remove sqlite database file before resetting migrations
```bash
$ rm -f tmp.db db.sqlite3
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
