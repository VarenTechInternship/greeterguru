# Greeter Guru

Greeter Guru is a "proof of concept" application designed, developed, and deployed by the Varen Technologies 2019 Internship Group. It is smart doorbell using facial recognition that unlocks the office and communicates with Slack to let other employees know that they are in the office and currently at work.

[![CircleCI](https://circleci.com/gh/VarenTechInternship/greeterguru.svg?style=svg)](https://circleci.com/gh/VarenTechInternship/greeterguru)


## Schematics

![Schematics](schematics.png)


## Features

* Detects and recognizes faces at office door to allow entrance to registered employees.

* Admin website for viewing and maintaining registered employees and saved pictures.

* Employee website for viewing any necessary login information.

* Integration with Active Directory to allow automatic employee registration.


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

NOTE: To uninstall OpenCV and the virtual environment run the following command - this may be necessary if the installation process fails partway through
```bash
$ bin/uninstall.sh
```


## How to Use

Set up connection to active directory
```bash
$ sudo sed -i '/TLS_REQCERT never/d' /etc/ldap/ldap.conf
$ sudo echo "TLS_REQCERT never" >> /etc/ldap/ldap.conf
```

Initialize active directory and web server information
```bash
$ bin/setup.sh
```

Run the application - you will have to enter the web admin's password
```bash
$ python3 launch.py
```


## Directories Overview

**FaceID:** Face detection and recognition package. Implements bulk of project's functionality.

--> **Datset:** Pictures of each employee.

--> **Cascade:** Reference file for face detection.

--> **Trainer:** Results from training the model.

**GGProject:** Root directory of GreeterGuru website.

--> **GreeterGuru:** Website project package.

--> **workflow:** Web application. Defines database objects.

   --> **management/commands:** Custom commands for web application.

--> **api:** Web application. Implements necessary APIs.

--> **scripts:** Additional python scripts for website.

**bin:** Bash scripts for installing and implementing various parts of the application.

**.circleci:** CircleCI directory. Used to automate testing.

**venv:** Virtual environment.
