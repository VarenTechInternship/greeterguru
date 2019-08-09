#!/bin/bash

echo "
INSTALLING MOST RECENT VERSION OF NUMPY:"
while [ "$numpy" != "y" ]; do
    pip3 install numpy
    read -r -p "Did numpy install successfully? (y/n): " numpy
done

echo "
CONFIGURING INSTALLATION:"
cd ~/opencv
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D INSTALL_PYTHON_EXAMPLES=ON \
      -D INSTALL_C_EXAMPLES=OFF \
      -D OPENCV_ENABLE_NONFREE=ON \
      -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
      -D PYTHON_EXECUTABLE=~/.virtualenvs/cv/bin/python \
      -D BUILD_EXAMPLES=ON ..

echo "
INCREASING THE SWAP ON THE RASPBERRY PI:"
sudo sed -i 's/CONF_SWAPSIZE=100/CONF_SWAPSIZE=2048/' /etc/dphys-swapfile
sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start

echo "
COMPILING OPENCV - THIS WILL TAKE ABOUT AN HOUR:"
sudo make -j4

echo "
INSTALLING OPENCV:"
sudo make install
sudo ldconfig

echo "
RESETTING THE SWAP ON THE RASPBERRY PI:"
sudo sed -i 's/CONF_SWAPSIZE=2048/CONF_SWAPSIZE=100/' /etc/dphys-swapfile
sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start

echo "
VERIFYING OPENCV VERSION - SHOULD DISPLAY '3.4.4':"
pkg-config --modversion opencv

echo "
LINKING OPENCV TO PYTHON VIRTUAL ENVIRONMENT:"
cd ~/.virtualenvs/cv/lib/python3.5/site-packages/
sudo ln -s /usr/local/python/cv2/python-3.5/cv2.cpython-35m-arm-linux-gnueabihf.so cv2.so

cd $GGPATH    # Return to GreeterGuru repo location

echo "
VERIFYING INSTALLATION - SHOULD DISPLAY '3.4.4':"
python3 bin/verify.py

echo "
INSTALLING PACKAGES WITH REQUIREMENTS:"
pip3 install -r requirements.txt
python3 -m pip install python-ldap
