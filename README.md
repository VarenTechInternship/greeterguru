# Greeter Guru
[![CircleCI](https://circleci.com/gh/VarenTechInternship/greeterguru.svg?style=svg)](https://circleci.com/gh/VarenTechInternship/greeterguru)

## Schematics

![Schematics](schematics.png)

## Installation

Update tools:
```bash
$ cd ~ && sudo apt-get update && sudo apt-get upgrade 
```
Install image processing and display packages:
```bash
$ sudo apt-get install -y libjpeg-dev build-essential cmake unzip pkg-config libjpeg-dev libpng-dev libtiff-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libgtk-3-dev libatlas-base-dev gfortran python3-dev python3-testresources
```
Get OpenCV packages and Pip:
```bash
$ cd ~ && wget -O opencv.zip https://github.com/opencv/opencv/archive/3.4.4.zip && wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/3.4.4.zip && unzip opencv.zip && unzip opencv_contrib.zip && mv opencv-3.4.4 opencv && mv opencv_contrib-3.4.4 opencv_contrib && wget https://bootstrap.pypa.io/get-pip.py && sudo python3 get-pip.py 
```
Set up and enter virtual environment:
```bash
$ sudo pip3 install virtualenv virtualenvwrapper && sudo rm -rf ~/get-pip.py ~/.cache/pip && sudo nano ~/.profile && source ~/.profile && mkvirtualenv cv -p python3 && workon cv
```
Copy and paste the following into the last line of the opened file:
```
# virtualenv and virtualenvwrapper
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source /usr/local/bin/virtualenvwrapper.sh
```
Install numpy and configure installation - numpy should be listed under the python3 section in the output:
```bash
$ pip install numpy && cd ~/opencv && mkdir build && cd build && cmake -D CMAKE_BUILD_TYPE=RELEASE \
-D CMAKE_INSTALL_PREFIX=/usr/local \
-D INSTALL_PYTHON_EXAMPLES=ON \
-D INSTALL_C_EXAMPLES=OFF \
-D OPENCV_ENABLE_NONFREE=ON \
-D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
-D PYTHON_EXECUTABLE=~/.virtualenvs/cv/bin/python \
-D BUILD_EXAMPLES=ON ..
```
Increase the SWAP on the Raspberry Pi - in the opened file, set CONF_SWAPSIZE to 2048:
```bash
$ sudo nano /etc/dphys-swapfile && sudo /etc/init.d/dphys-swapfile stop && sudo /etc/init.d/dphys-swapfile start
```
Compile and install OpenCV 4 - this will take about 45 minutes:
```bash
$ make -j4 && sudo make install && sudo ldconfig
```
Reset the SWAP on the Raspberry Pi - in the opened file, set CONF_SWAPSIZE back to 100:
```bash
$ sudo nano /etc/dphys-swapfile && sudo /etc/init.d/dphys-swapfile stop && sudo /etc/init.d/dphys-swapfile start
```
Link OpenCV to Python virtual environment:
```bash
$ cd ~/.virtualenvs/cv/lib/python3.5/site-packages/ && ln -s /usr/local/python/cv2/python-3.5/cv2.cpython-35m-arm-linux-gnueabihf.so cv2.so && cd ~
```
Verify the new installation in python interpreter - should display “3.4.4”:
```bash
$ python
```
```python
>>> import cv2
>>> cv2.__version__ 
>>> exit()
```
Install required packages in virtual environment:
```bash
$ pip3 install -r requirements.txt
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