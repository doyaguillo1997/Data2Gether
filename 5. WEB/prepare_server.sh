sudo apt update

# Python dependences
sudo apt -y install python3-pip
sudo apt -y install python3-venv
pip install --user pipenv

# BBDD dependences
sudo apt -y install postgresql
sudo apt -y install postgis postgresql-12-postgis-3

# Deploy dependences
sudo apt -y install uwsgi
sudo apt -y install gunicorn 
sudo apt -y install nginx
sudo apt -y install net-tools

# Prepare BBDD
sudo su postgres -c "psql -c \"CREATE USER \"data2gether\"\""
sudo su postgres -c "psql -c \"CREATE DATABASE \"data2gether\" OWNER \"data2gether\" ENCODING 'UTF-8'\"";
sudo -u postgres -- psql -d "data2gether" -c "CREATE EXTENSION IF NOT EXISTS postgis;"
sudo -u postgres -- psql -d "data2gether" -c "ALTER USER data2gether WITH PASSWORD 'data2gether';"

# Map config files and run
cd ..
sudo ln -sT /home/ubuntu/data2gether/etc/gunicorn.service /etc/systemd/system/gunicorn.service
sudo ln -sT /home/ubuntu/data2gether/etc/gunicorn.socket /etc/systemd/system/gunicorn.socket

sudo ln -sT /home/ubuntu/data2gether/etc/nginx.conf /etc/nginx/sites-enabled/data2gether.conf
