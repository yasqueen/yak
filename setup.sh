#!/bin/sh

apt-get install python-dev python-pip nginx
pip install --upgrade pip
pip install virtualenv uwsgi


# Create a directory for the UNIX sockets
mkdir /var/run/yak
chown www-data:www-data /var/run/yak

# Create a directory for the logs
mkdir /var/log/yak
chown www-data:www-data /var/log/yak

# Create a directory for the configs
mkdir /etc/yak

# Virtualenv
virtualenv yakenv
source yakenv/bin/activate
pip install -r requirements.txt

# Copy conf files
cp yak.conf /etc/init/
cp yak.ini /etc/yak/

# Nginx set up
rm /etc/nginx/sites-enabled/default
cp yaksite /etc/nginx/sites-available/
ln -sf /etc/nginx/sites-available/yaksite /etc/nginx/sites-enabled

# start service
service yak start
service nginx reload