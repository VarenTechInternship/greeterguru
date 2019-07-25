#!/bin/bash

cp bin/base_crontab_file bin/crontab

read -r -p "Would you like the web database to automatically update every minute (m), hour (h), day (d), or never (n): " update

if [ "$update" = "m" ]
then
    echo "* * * * * python3 $PWD/GGProject/manage.py sync_command" >> bin/crontab
elif [ "$update" = "h" ]
then
    echo "0 * * * * python3 $PWD/GGProject/manage.py sync_command" >> bin/crontab
elif [ "$update" = "d" ]
then
    echo "0 0 * * * python3 $PWD/GGProject/manage.py sync_command" >> bin/crontab
elif [ "$update" = "n" ]
then
    echo "" >> bin/crontab
else
    echo "That is not an option."
fi

crontab bin/crontab
rm bin/crontab
