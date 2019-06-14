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
$ cd GreeterGuru && pip3 install -r requirements.txt
```

## Directories Overview

FaceID: Face detection and recognition package. Implements bulk of project's functionality.

GGProject: Root directory of GreeterGuru Django project.

GreeterGuru: Django project package.

main: Django application. Handles project workflow.

api: Django application. Implements necessary APIs.

scripts: Additional python scripts for Django project.

.circleci: CircleCI directory. Used to automate testing.

venv: Virtual environment.