#!/bin/bash

echo "
RUNNING OPENCV'S MAKE UNINSTALL COMMAND:"
cd ~/opencv/build/
sudo make uninstall

echo "
VERIFYING THE RASPBERRY PI'S SWAP WAS RESET:"
sudo sed -i 's/CONF_SWAPSIZE=2048/CONF_SWAPSIZE=100/' /etc/dphys-swapfile
sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start

echo "
DELETING CREATED VIRTUAL ENVIRONMENT:"
sudo rm -rf ~/.virtualenvs/cv/

echo "
REMOVING VIRTUAL ENVIRONMENT SETTINGS IN ~/.PROFILE:"
sudo sed -i '/# virtualenv and virtualenvwrapper/d' ~/.profile
sudo sed -i '/export WORKON_HOME=$HOME\/.virtualenvs/d' ~/.profile
sudo sed -i '/export VIRTUALENVWRAPPER_PYTHON=\/usr\/bin\/python3/d' ~/.profile
sudo sed -i '/source \/usr\/local\/bin\/virtualenvwrapper.sh/d' ~/.profile

echo "
REMOVING OPENCV DIRECTORIES AND FILES:"
sudo rm -rf ~/opencv/
sudo rm -rf ~/opencv_contrib/
