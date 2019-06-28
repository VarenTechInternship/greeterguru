# Greeter Guru
[![CircleCI](https://circleci.com/gh/VarenTechInternship/greeterguru.svg?style=svg)](https://circleci.com/gh/VarenTechInternship/greeterguru)
## Schematics

![Schematics](schematics.png)

## Installation

Updating tools:
```bash
$ cd ~
$ sudo apt-get update && sudo apt-get upgrade 
```
Install image processing and display packages:
```bash
$ sudo apt-get install build-essential cmake unzip pkg-config 
$ sudo apt-get install libjpeg-dev libpng-dev libtiff-dev 
$ sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev  
$ sudo apt-get install libxvidcore-dev libx264-dev 
$ sudo apt-get install libgtk-3-dev 
$ sudo apt-get install libatlas-base-dev gfortran 
$ sudo apt-get install python3-dev python3-testresources
```
Get OpenCV packages:
```bash
$ cd ~
$ wget -O opencv.zip https://github.com/opencv/opencv/archive/3.4.4.zip 
$ wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/3.4.4.zip
$ unzip opencv.zip && unzip opencv_contrib.zip 
$ mv opencv-3.4.4 opencv && mv opencv_contrib-3.4.4 opencv_contrib 
```
Install Pip:
```bash:
$ wget https://bootstrap.pypa.io/get-pip.py 
$ sudo python3 get-pip.py 
```
Create virtual environment:
```bash
$ sudo pip3 install virtualenv virtualenvwrapper 
$ sudo rm -rf ~/get-pip.py ~/.cache/pip 
$ sudo nano ~/.bashrc
```
Copy and paste the following into the last line of the opened file:
```
# virtualenv and virtualenvwrapper
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source /usr/local/bin/virtualenvwrapper.sh
```
Enter the virtual machine:
```bash
$ source ~/.bashrc
$ mkvirtualenv cv -p python3
$ workon cv
```
Configuring and compiling (from now on, (cv) should be displayed before username):
```bash
$ pip install numpy
$ workon cv
$ cd ~/opencv
$ mkdir build && cd build
$  cmake -D CMAKE_BUILD_TYPE=RELEASE \
	-D CMAKE_INSTALL_PREFIX=/usr/local \
	-D INSTALL_PYTHON_EXAMPLES=ON \
	-D INSTALL_C_EXAMPLES=OFF \
	-D OPENCV_ENABLE_NONFREE=ON \
	-D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
	-D PYTHON_EXECUTABLE=~/.virtualenvs/cv/bin/python \
	-D BUILD_EXAMPLES=ON ..
```
Install OpenCV 4 (this will take about 30 minutes):
```bash
$ make -j4
```
Verify OpenCV version - output should show "3.4.4":
```bash
$ sudo make install && sudo ldconfig
$ pkg-config --modversion opencv
```
Verify Python version - output should show "cv2.cpython-36m-x86_64-linux-gnu.so":
```bash
$ ls /usr/local/python/cv2/python-3.6
```
Relocate necessary files:
```bash
$ cd /usr/local/python/cv2/python-3.6
$ sudo mv cv2.cpython-36m-x86_64-linux-gnu.so cv2.so
$ cd ~/.virtualenvs/cv/lib/python3.6/site-packages/
$ ln -s /usr/local/python/cv2/python-3.6/cv2.so cv2.so
```
Test installation:
```bash
$ cd ~
$ workon cv
$ python
```
Verify installation - should print "3.4.4"
```python
import cv2
cv2.__version__ 
```
Install packages with requirements:
```bash
pip3 install -r requirements.txt
```

## Running the Application
```bash
$ cd GGProject && python3 manage.py runserver
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