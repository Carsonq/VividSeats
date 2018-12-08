sudo mkdir /usr/local/include
sudo chown -R `whoami`:admin /usr/local/include
sudo mkdir /usr/local/lib
sudo chown -R `whoami`:admin /usr/local/lib
sudo mkdir /usr/local/sbin
sudo chown -R `whoami`:admin /usr/local/sbin

brew install mysql
brew services start mysql
alias mysql=/usr/local/opt/mysql/bin/mysql
alias mysqladmin=/usr/local/opt/mysql/bin/mysqladmin
mysqladmin --user=root password "root"
sudo easy_install pip
export PATH=$PATH:/usr/local/opt/mysql/bin
pip install MySQL-python
