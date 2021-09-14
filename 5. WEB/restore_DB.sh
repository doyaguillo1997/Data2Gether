sudo su postgres -c "dropdb data2gether"
sudo su postgres -c "psql -c \"CREATE DATABASE \"data2gether\" OWNER \"data2gether\" ENCODING 'UTF-8'\"";
sudo -u postgres -- psql -d "data2gether" -c "CREATE EXTENSION IF NOT EXISTS postgis;"
sudo su postgres -c "pg_restore -d "data2gether" --no-owner --role "data2gether" -j 8 "dump-d2g""
