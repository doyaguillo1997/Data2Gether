# ¡Bienvenidos al repositorio de Data!

Aqui podemos subir los comandos de git que nos parezcan útiles modificando el archivo.

# Dependencias

Instalar estos paquetes:

* Python
* Postgres
* Postgis

Las instrucciones varían según sistema operativo.

## Pipenv

Una vez instalado Python en el sistema operativo, ejecutar:

```
pip install --user pipenv
```

Referencias: https://pipenv.pypa.io/en/latest/#install-pipenv-today

# Instalación

## Base de datos

Para que nuestra aplicación pueda trabajar en local con postgis sera necesario ejecutar las siguientes instrucciones dentro de postgres.

1. Crear la base de datos:

```
$ sudo -u postgres psql
CREATE USER "data2gether"
CREATE DATABASE "data2gether" OWNER "data2gether" ENCODING 'UTF-8';
```

2. Habilitar la extensión Postgis en data2gether:

```
$ sudo -u postgres -- psql -d "data2gether"
CREATE EXTENSION IF NOT EXISTS postgis;
```

## Paquetes del proyecto

Mediante el paquete pipenv podremos instalar todas las dependencias internas del proyecto:

```
pipenv install -d
```

## Django Admin

Django ofrece una capa para la gestión de la base de datos. Para ello es necesario crear un superusuario:

```
# Activar entorno 
pipenv shell
# Crear superusario
python3 manage.py createsuperuser --username=admin 
```

# Arranque

Entrar en el entorno virtual

```
pipenv shell
```

Ejecutar Django runserver:

```
python manage.py runserver
```

Entrar en http://locahost:8000/

# Comandos 

Siturse en la carpeta App

## Load Cadastre

Carga la informacion catastral sobre las viviendas de una cartera

```
python manage.py id_load
```

# Producción

## Conexion

Habilitar clave SSH en el servidor.

Conectarse mediante ssh

```
ssh ...
```

## Instalar dependencias

```
./data2gether/prepare_server.sh
```

## Cargar BBDD

Obtener y subir dump al servidor

```
cd /var/lib/postgresql/
sudo su postgres
pg_dump -Fc data2gether -f "dump-d2g"
mv dump-d2g /tmp/
```

```
scp /tmp/dump-d2g data2gether.com:/home/ubuntu/
```

Cargar dump en la base de datos del servidor

```
./restore_DB.sh
```

## Despligue

```
./deployment.sh
```
