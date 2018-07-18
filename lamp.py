#!/usr/bin/env python3
#coding=utf-8

import os
import shutil
import configparser
import mysql.connector

#update

print ("Checking updates")
os.system('apt update')

#upgrade

print ("Installing updates")
os.system('apt upgrade -y')

#install packages

print ("Installing packages")
os.system('apt install apache2 mysql-server php7.2 libapache2-mod-php7.2 php-mysql python3-mysql.connector -y')
    

#configure apache2

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
'''
f = open("/etc/apache2/mods-available/mpm_prefork.conf", 'r')
f1 = open("/etc/apache2/mods-available/~mpm_prefork.conf", 'w')

filetext = f.readlines()
filetext.remove('\tStartServers\t\t\t 5\n')
filetext.insert(8,'\tStartServers\t\t\t 4\n')
filetext.remove('\tMinSpareServers\t\t  5\n')
filetext.insert(9,'\tMinSpareServers\t\t  3\n')
filetext.remove('\tMaxSpareServers\t\t 10\n')
filetext.insert(10,'\tMaxSpareServers\t\t 40\n')
filetext.remove('\tMaxRequestWorkers\t  150\n',)
filetext.insert(11,'\tMaxRequestWorkers\t  200\n',)
filetext.remove('\tMaxConnectionsPerChild   0\n')
filetext.insert(12,'\tMaxConnectionsPerChild  10000\n')

f1.writelines(filetext)
f.close()
f1.close()

os.rename('/etc/apache2/mods-available/~mpm_prefork.conf', '/etc/apache2/mods-available/mpm_prefork.conf')
'''
# Disable the event module and enable prefork
print("Disable the event module and enable prefork")

os.system('a2dismod mpm_event')
os.system('a2enmod mpm_prefork')

#Restart Apache

print("Restart Apache")

os.system('systemctl restart apache2')


#Virtual Hosts
#Create a copy of the default Apache configuration file for your site

print("Create a copy of the default Apache configuration file for your site")

shutil.copy2('/etc/apache2/sites-available/000-default.conf', '/etc/apache2/sites-available/example.com.conf')


f = open("/etc/apache2/sites-available/example.com.conf", 'w')

f.writelines(['<Directory /var/www/html/example.com/public_html>\n', 
'        Require all granted\n', 
'</Directory>\n', '<VirtualHost *:80>\n', 
'        ServerName example.com\n', 
'        ServerAlias www.example.com\n', 
'        ServerAdmin webmaster@localhost\n', 
'        DocumentRoot /var/www/html/example.com/public_html\n', '\n',
'        ErrorLog /var/www/html/example.com/logs/error.log\n',
'        CustomLog /var/www/html/example.com/logs/access.log combined\n', 
'\n','</VirtualHost>'])

f.close()
 
 
#Create a public_html and a log directory

print("Create a public_html and a log directory")
 

if not os.path.exists("/var/www/html/example.com/public_html"):
    os.makedirs("/var/www/html/example.com/public_html")
os.system('chown www-data /var/www/html/example.com/public_html')
    
if not os.path.exists("/var/www/html/example.com/logs"):
    os.makedirs("/var/www/html/example.com/logs")
os.system('chown www-data /var/www/html/example.com/logs')
#Reload configuration

print("Reload configuration")
os.system('systemctl reload apache2')
os.system('a2ensite example.com')
os.system('a2dissite 000-default.conf')
os.system('systemctl reload apache2')



#Connect to the mysql shell, with unix_socket defined  (https://stackoverflow.com/questions/6885164/pymysql-cant-connect-to-mysql-on-localhost), otherwise we will get "Access denied for user 'root'@'localhost'" error
print("Configure mysql")
cnx = mysql.connector.connect(unix_socket='/var/run/mysqld/mysqld.sock', user='root')
cursor=cnx.cursor()
#Sql for creating "webdata" database
database = "CREATE DATABASE IF NOT EXISTS webdata"
#Sql for creating user "webuser" and password
user = "GRANT ALL ON webdata.* TO 'webuser' IDENTIFIED BY 'password'"
#Automating mysql_secure_installation
disable_remote_root ="DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1')"
remove_ano_users = "DELETE FROM mysql.user WHERE User=''"
remove_test = "DELETE FROM mysql.db WHERE Db='test' OR Db='test_%'"
reload_privilages = "FLUSH PRIVILEGES"
cursor.execute(database)
#The result of  cursor.execute(database) command (useful for debugging)
print(cursor.statement)
cursor.execute(user)
print(cursor.statement)
cursor.execute(disable_remote_root)
print(cursor.statement)
cursor.execute(remove_ano_users)
print(cursor.statement)
cursor.execute(remove_test)
print(cursor.statement)
cursor.execute(reload_privilages)
print(cursor.statement)
cnx.close()


#Edit /etc/php/7.2/apache2/php.ini

print("Edit /etc/php/7.2/apache2/php.ini")
config = configparser.ConfigParser()
config.read('/etc/php/7.2/apache2/php.ini')
config.set('PHP','error_reporting','E_COMPILE_ERROR | E_RECOVERABLE_ERROR | E_ERROR | E_CORE_ERROR')
config.set('PHP','max_input_time','30')
config.set('PHP','error_log', '/var/log/php/error.log')
#All comments will be removed from the /etc/php/7.2/apache2/php.ini file
configfile = open('/etc/php/7.2/apache2/php.ini', 'w')
config.write(configfile)
configfile.close()
# as an alternative you can use
#with open('/etc/php/7.2/apache2/php.ini', 'w') as configfile:
#        config.write(configfile)

if not os.path.exists('/var/log/php'):
    os.system('mkdir /var/log/php')
os.system('chown www-data /var/log/php')
os.system('systemctl restart apache2')

print("Configuration of the lamp stack completed")

#Optionally test our lamp stack

'''
print("Optionally test our lamp stack")

t = open("/var/www/html/example.com/public_html/phptest.php", 'w')

t.writelines(['<html>\n', 
'<head>\n', 
'    <title>PHP Test</title>\n', '</head>\n', '    <body>\n',
"    <?php echo '<p>Hello World</p>';\n", '\n',
'    // In the variables section below, replace user and password with your own MySQL credentials as created on your server\n', 
'    $servername = "localhost";\n', '    $username = "webuser";\n', '    $password = "password";\n', '\n',
'    // Create MySQL connection\n', '    $conn = mysqli_connect($servername, $username, $password);\n', '\n', 
'    // Check connection - if it fails, output will include the error message\n','    if (!$conn) {\n', 
"        die('<p>Connection failed: <p>' . mysqli_connect_error());\n", '    }\n', 
"    echo '<p>Connected successfully</p>';\n", '    ?>\n', '</body>\n', '</html>\n'])

t.close()

os.system('su - luc -c "xdg-open http://localhost/phptest.php" && rm /var/www/html/example.com/public_html/phptest.php')
'''


 
 
 
 
