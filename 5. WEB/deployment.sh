cd data2gether

# Get last changes
git pull

# Install packages dependences
pipenv install

# Prepare statics
./manage.py collectstatic --no-input --clear --no-post-process

# Restart services
sudo systemctl daemon-reload
sudo systemctl restart gunicorn.service
sudo nginx -t 
sudo nginx -s reload
