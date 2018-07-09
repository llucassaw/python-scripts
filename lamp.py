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

#configure /etc/apache2/mods-available/mpm_prefork.conf 

print("configuring /etc/apache2/mods-available/mpm_prefork.conf")

f = open("/etc/apache2/mods-available/~mpm_prefork.conf", 'w')

f.writelines(['# prefork MPM\n',
'# StartServers: number of server processes to start\n',
'# MinSpareServers: minimum number of server processes which are kept spare\n',
'# MaxSpareServers: maximum number of server processes which are kept spare\n',
'# MaxRequestWorkers: maximum number of server processes allowed to start\n', 
'# MaxConnectionsPerChild: maximum number of requests a server process serves\n',
'\n', '<IfModule mpm_prefork_module>\n', 
'\tStartServers\t\t\t 4\n', '\tMinSpareServers\t\t  3\n', '\tMaxSpareServers\t\t 40\n', '\tMaxRequestWorkers\t  200\n', '\tMaxConnectionsPerChild   10000\n',
 '</IfModule>\n', '\n', '# vim: syntax=apache ts=4 sw=4 sts=4 sr noet\n'])
 
f.close()
 
os.rename('/etc/apache2/mods-available/~mpm_prefork.conf', '/etc/apache2/mods-available/mpm_prefork.conf')
 
 #Alternative method with lists
 
# f = open("/etc/apache2/mods-available/mpm_prefork.conf", 'r')
#f1 = open("/etc/apache2/mods-available/~mpm_prefork.conf", 'w')

#filetext = f.readlines()
#filetext.remove('\tStartServers\t\t\t 5\n')
#filetext.insert(8,'\tStartServers\t\t\t 4\n')
#filetext.remove('\tMinSpareServers\t\t  5\n')
#filetext.insert(9,'\tMinSpareServers\t\t  3\n')
#filetext.remove('\tMaxSpareServers\t\t 10\n')
#filetext.insert(10,'\tMaxSpareServers\t\t 40\n')
#filetext.remove('\tMaxRequestWorkers\t  150\n',)
#filetext.insert(11,'\tMaxRequestWorkers\t  200\n',)
#filetext.remove('\tMaxConnectionsPerChild   0\n')
#filetext.insert(12,'\tMaxConnectionsPerChild  10000\n')

#f1.writelines(filetext)
#f.close()
#f1.close()

#os.rename('/etc/apache2/mods-available/~mpm_prefork.conf', '/etc/apache2/mods-available/mpm_prefork.conf')

# Disable the event module and enable prefork
print("Disable the event module and enable prefork")

os.system('sudo a2dismod mpm_event')
os.system('sudo a2enmod mpm_prefork')

#Restart Apache

print("Restart Apache")

os.system('sudo systemctl restart apache2')

