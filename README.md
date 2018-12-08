Work on Ubuntu 18.04

sudo apt-get update
sudo apt-get install mysql-server
sudo service mysql start

login to mysql "sudo mysql -u root"
execute: ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';
log out.

mysql -u root -p < vivid.sql
sudo apt-get install python-mysqldb
sudo apt-get install python-pip

pip install Flask
pip install Flask-SQLAlchemy
pip install flask-jsonpify

python populate_tables.py
