# Data2Gether

Este es el repositorio de código del proyecto Data2Gether. Nace de un Trabajo de Fin de Máster para la UCM.

El proyecto se ha llevado a cabo bajo una idea básica de negocio, la cual  consiste en desarrollar e implementar una solución en forma de aplicación WEB que tenga incorporada modelos de predicción de precios de inmuebles para la ciudad de Madrid, bajo los requerimientos de FI inmobiliarios, en el mercado actual (abril 2021).

Queda dividido en cinco partes:

## 1. Recolección de datos

Este repositorio recoge los scripts utilizados para la recolección de datos de las siguientes fuentes:

	- Idealista API
	
	- Idealista WEB
	
	- MiCole WEB
	
	- Places API (Google Maps Platform)

## 2. Depuración de datos

Aquí se recogen los scripts desarrollados para el análisis y el procesado de los datos obtenidos.

## 3. Modelos de regresión

El repositorio contiene operaciones de transformación de los datos obtenidos (recogidos en un pipeline con transformadores personalizados) y el proceso de comparación, selección y generación de modelos de regresión.

## 4. Series temporales

En este apartado, el único programado en R, se ajusta un modelo de series temporales a cada serie de precios medios por metro cuadrado de los distritos del municipio de Madrid (además de a la serie correspondiente al municipio de Madrid en conjunto).

## 5. WEB

Contiene el código de la aplicación WEB. Como se ha comentado en la memoria, es una aplicación hecha en Django. Este repositorio contiene tanto front como back, así como ficheros de despligue, de configuración de entorno y los paquetes creados durante el pipeline del modelo.
