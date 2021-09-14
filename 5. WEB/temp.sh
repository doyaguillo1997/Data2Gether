##### Local #####
# Connect to postgreSQL
sudo -u postgres psql

# Make dump and move to local folder
pg_dump -Fc data2gether -f "dump-d2g"
mv dump-d2g /tmp/
# Ctrl+d

# Copy dump into server
scp /tmp/dump-d2g data2gether2gb.com:/home/ubuntu/
# Copy model file into server
scp app/model_files/GOATModel_RandomForestRegressor.pkl data2gether2gb.com:/home/ubuntu/data2gether/app/

##### Server #####
# Update 
sudo apt update

# Clone Repository
git clone git@gitlab.com:data2gether.dr/data2gether.git

# Install packages dependences and project packages
cd data2gether
sudo apt install python3-pip
sudo apt install python3-venv
pip install --user pipenv
pipenv install

# Load Model File
cd app
mkdir model_files
cd ..
mv GOATModel_RandomForestRegressor.pkl app/model_files

# Create static files
./manage.py collectstatic --no-input --clear --no-post-process



# Install BBDD and extensions
sudo apt install postgresql
sudo apt install postgis postgresql-12-postgis-3
sudo su postgres
CREATE USER "data2gether"
CREATE DATABASE "data2gether" OWNER "data2gether" ENCODING 'UTF-8';
# Ctrl+d
sudo -u postgres -- psql -d "data2gether"
CREATE EXTENSION IF NOT EXISTS postgis;
ALTER USER data2gether WITH PASSWORD 'data2gether';
# Ctrl+d
sudo su postgres
pg_restore -d "data2gether" --no-owner --role "data2gether" -j 8 "dump-d2g"

# Gunicorn (start service)
sudo apt install uwsgi
sudo apt install gunicorn 
# Map configuration files
sudo ln -sT /home/ubuntu/data2gether/etc/gunicorn.service /etc/systemd/system/gunicorn.service
sudo ln -sT /home/ubuntu/data2gether/etc/gunicorn.socket /etc/systemd/system/gunicorn.socket
# Start service
sudo systemctl daemon-reload
sudo systemctl enable gunicron.service # active servic always

# Nginx
sudo apt install nginx
# Map configuration file
sudo ln -sT /home/ubuntu/data2gether/etc/nginx.conf /etc/nginx/sites-enabled/data2gether.conf
# Restart service
sudo nginx -t && nginx -s reload


##### Extra Packages #####

# See service logs
journalctl -f -u gunicorn.service
journalctl -f -u nginx.service

# See open files
sudo lsof # All
sudo lsof | grep '^gunicorn' # Gunircon files opened

# See Nginx logs
sudo tail -f  /var/log/nginx/access.log  /var/log/nginx/error.log # All
sudo tail -n100 -f  /var/log/nginx/access.log  /var/log/nginx/error.log #Only 100 logs 

# IP Info
curl http://ipinfo.io # Public IP
ifconfig # Private IP. Needs package -> sudo apt install net-tools

# Rename commit athor
git commit --amend --author "Biel Arenas <biel.arenas@gmail.com>"

34.243.60.56

# Cambiar
# Restore DB
# Deploy
# Logs gUNI
# Logs Nginx
# Install server dependeces
