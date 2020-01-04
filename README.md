README Cavaliba
===============


---------------------------------------------------------------------
Memento
---------------------------------------------------------------------

start cavaliba
--------------
export CAVALIBA_DBPWD=xxx
python3 manage.py runserver


create superuser
----------------
python3 manage.py createsuperuser
admin / *****************
   => 127.0.0.1/admin

---------------------------------------------------------------------
Install Mysql
---------------------------------------------------------------------

sudo apt-get install mariadb-server
mysql -V
sudo apt-get install python3-dev
sudo apt-get install python3-dev libmysqlclient-dev
sudo python3 -m pip install mysqlclient

mysql -u root -p

CREATE DATABASE cavaliba_dev CHARACTER SET utf8 COLLATE utf8_bin;
grant all privileges on cavaliba_dev.* to cavaliba_dev@localhost identified by 'xxx';
FLUSH PRIVILEGES;

SELECT User,Host FROM mysql.user;
SHOW GRANTS FOR 'cavaliba_dev'@'localhost';

---------------------------------------------------------------------
Install App Cavaliba
---------------------------------------------------------------------
install Django...

git clone ssh://boss@marcy.paturel.net:/data/phil/Git/cavaliba.git

cd cavaliba

settings.py :

SECRET_KEY
ALLOWED_HOSTS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cavaliba_dev',
        'USER': 'cavaliba_dev',
        'PASSWORD': 'XXX',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}


export CAVALIBA_DBPWD=xxx

python3 manage.py makemigrations
python3 manage.py migrate

python3 manage.py createsuperuser
   => http://127.0.0.1:8000/admin

python3 manage.py runserver
   => http://127.0.0.1:8000



