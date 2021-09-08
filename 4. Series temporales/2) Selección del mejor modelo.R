#Script para seleccionar el mejor modelo de cada barrio

setwd("C:/Users/Borja/Documents/Universidad/Master/TFM/Series Distritos/Datos")
source("../0) Funciones Necesarias.R")
ficheros <- c(list.files()[2:9], list.files()[11:24])


#Primero, obtengo el mejor modelo de cada tipo, obviando el ensamblado (ya que este se va a hacer a 
#partir del mejor modelo de cada tipo que se obtenga ahora):
for(fichero in ficheros){
  MejorModelo <- mejor_modelo(fichero, "2006-01-01", "2021-07-01", 19, 1)
  save(MejorModelo, 
       file = paste0("../Mejores modelos de cada tipo/", 
                     substr(fichero, 1, nchar(fichero) - 5), ".RData"))
}


#Ahora, obtengo el mejor ensamblado:
for(fichero in ficheros){
  MejorModelo <- mejor_ensamblado(fichero, "2006-01-01", "2021-07-01", 19, 1)
  save(MejorModelo, 
       file = paste0("../Mejores modelos de cada tipo/", 
                     substr(fichero, 1, nchar(fichero) - 5), ".RData"))
}

#Finalmente, obtengo cual es el mejor modelo de todos, para cada distrito:
for(fichero in ficheros){
  MejorModelo <- mejor_modelo_final(fichero, "2006-01-01", "2021-07-01", 19, 1)
  save(MejorModelo, 
       file = paste0("../Mejor modelo final/", 
                     substr(fichero, 1, nchar(fichero) - 5), ".RData"))
}
