#!/usr/bin/env python3
#coding=utf-8

import os

#updating

def update_function():

    print ("Checking updates")
    os.system('sudo apt update')

update_function()

#upgrade

def upgrade_function():

    print ("Installing updates")
    os.system('sudo apt upgrade -y')

upgrade_function()

#installing packages

def install_function():

    print ("Installing packages")
    os.system('sudo apt install apache2 mysql-server php7.2 libapache2-mod-php7.2 php-mysql -y')

install_function()

#configuring apache2
print ("configuring apache")

f = open('/etc/apache2/apache2.conf','r')
filedata = f.read()
f.close()

newdata = filedata.replace('MaxKeepAliveRequests 100', 'MaxKeepAliveRequests 50')

f = open('/etc/apache2/apache2.conf','w')
f.write(newdata)
f.close()
