#Script que sirve para dividir las series de los barrios en un fichero por cada barrio,
#ya que todas las series venian en un unico fichero

library(openxlsx)
setwd("C:/Users/Borja/Documents/Universidad/Master/TFM/Series Distritos/Datos")

#Lectura y eliminacion de lo que no es distrito:
datos <- read.csv("historico_madrid.csv", sep = ",")
eliminar <- which(datos$Zona %in% c("madrid-comunidad", "madrid-provincia"))
datos <- datos[-eliminar, ]

#Corrijo los nombres malos:
datos$Zona <- ifelse(datos$Zona == "san-blas", "sanblas", 
                     ifelse(datos$Zona == "ciudad-lineal", "ciudadlineal",
                            ifelse(datos$Zona == "villa-de-vallecas", "villadevallecas",
                                   ifelse(datos$Zona == "puente-de-vallecas", "puentedevallecas", datos$Zona))))

#Spliteo por distritos:
distritos <- unique(datos$Zona)
for(distrito in distritos){
  df_aux <- datos[which(datos$Zona == distrito), c("Mes", "Precio.m2")]
  df_aux <- df_aux[nrow(df_aux):1, ]
  write.xlsx(df_aux, paste0(distrito, ".xlsx"))
}

