#!/bin/bash

echo "
UPDATING AND UPGRADING:"
cd ~
sudo apt-get -y update
sudo apt-get -y upgrade

echo "
INSTALLING NECESSARY PACKAGES:"
sudo apt-get install -y build-essential cmake unzip pkg-config libjpeg-dev libpng-dev libtiff-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libgtk-3-dev libatlas-base-dev gfortran python3-dev python3-testresources

echo "
RETRIEVING OPENCV PACKAGES:"
cd ~
sudo wget -O opencv.zip https://github.com/opencv/opencv/archive/3.4.4.zip
sudo wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/3.4.4.zip
unzip -q opencv.zip
unzip -q opencv_contrib.zip
mv opencv-3.4.4 opencv
mv opencv_contrib-3.4.4 opencv_contrib
rm -f opencv.zip
rm -f opencv_contrib.zip

echo "
GETTING AND INSTALLING PIP:"
sudo wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py

echo "
SETTING UP VIRTUAL ENVIRONMENT:"
sudo pip3 install virtualenv virtualenvwrapper
sudo rm -rf ~/get-pip.py ~/.cache/pip

# Remove the virtual environment settings if they've already been added
sudo sed -i '/# virtualenv and virtualenvwrapper/d' ~/.profile
sudo sed -i '/export WORKON_HOME=$HOME\/.virtualenvs/d' ~/.profile
sudo sed -i '/export VIRTUALENVWRAPPER_PYTHON=\/usr\/bin\/python3/d' ~/.profile
sudo sed -i '/source \/usr\/local\/bin\/virtualenvwrapper.sh/d' ~/.profile

# Insert the virtual environment settings in .profile
echo "# virtualenv and virtualenvwrapper" >> ~/.profile
echo "export WORKON_HOME=\$HOME/.virtualenvs" >> ~/.profile
echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.profile
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.profile
