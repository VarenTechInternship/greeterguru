#!/bin/bash

echo "
INITIALIZE ACTIVE DIRECTORY"
read -r -p "Address: " ad_name
read -r -p "Admin username: " ad_user
read -r -s -p "Password: " ad_pass1
echo
read -r -s -p "Confirm password: " ad_pass2
echo

# Confirm entered passwords match
while [ "$ad_pass1" != "$ad_pass2" ]; do
    echo "Passwords do not match"
    read -r -s -p "Re-enter password: " ad_pass1
    echo
    read -r -s -p "Confirm password: " ad_pass2
    echo
done

sed -i '/TLS_REQCERT never/d' /etc/ldap/ldap.conf
echo "TLS_REQCERT never" >> /etc/ldap/ldap.conf

echo "
INITIALIZE WEB DATABASE"
python3 GGProject/manage.py makemigrations
python3 GGProject/manage.py migrate

echo "INITIALIZE WEBSITE"
read -r -p "Address: " web_name
read -r -p "Admin username: " web_user
sed -i "s/WEB_ADDRESS = .*/WEB_ADDRESS = \"$web_name\"/" GGProject/GreeterGuru/settings.py
python3 GGProject/manage.py createsuperuser --username $web_user
sed -i "s/WEB_USERNAME = .*/WEB_USERNAME = \"$web_user\"/" GGProject/GreeterGuru/settings.py

# Initialize automatic updates
bin/update.sh

sudo sed -i "s/AD_NAME = .*/AD_NAME = \"$ad_name\"/" GGProject/GreeterGuru/settings.py
sudo sed -i "s/AD_USERNAME = .*/AD_USERNAME = \"$ad_user\"/" GGProject/GreeterGuru/settings.py
sudo sed -i "s/AD_PASSWORD = .*/AD_PASSWORD = \"$ad_pass1\"/" GGProject/GreeterGuru/settings.py
