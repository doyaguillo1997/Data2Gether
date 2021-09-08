#Script para hacer las predicciones de cada barrio, usando el modelo elegido en cada uno

library(openxlsx)
library(dplyr)
library(tibbletime)
library(timetk) 
library(tidymodels)
library(modeltime)
library(modeltime.ensemble)
setwd("C:/Users/Borja/Documents/Universidad/Master/TFM/Series Distritos/Datos")


########################################################################################################
########################################################################################################
###############################################ARGANZUELA###############################################
########################################################################################################
########################################################################################################
load("../Mejor modelo final/arganzuela.RData")

#Lectura:
fichero <- "arganzuela.xlsx"
datos <- read.xlsx(fichero) %>% 
  mutate(Mes = seq(from = as.Date("2006-01-01"), to = as.Date("2021-07-01"), by = 'month')) %>%
  as_tbl_time(index = Mes) %>% rename(Precio = Precio.m2) %>% filter(!is.na(Precio))

#Predicciones:
calibration_table <- MejorModelo %>%
  modeltime_calibrate(datos)
predicciones <- calibration_table %>% 
  modeltime_forecast(h = "24 months", actual_data = datos) 
calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  plot_modeltime_forecast(.interactive = FALSE)

#Escritura:
predicciones <- calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  rename(Fecha = .index, Valor = .value, ConfLow = .conf_lo, ConfUp = .conf_hi,
         TipoValor = .key) %>% select(c(Fecha, TipoValor, Valor, ConfLow, ConfUp)) %>%
  mutate(Valor = round(Valor))
write.xlsx(predicciones, "../Predicciones/arganzuela.xlsx")



########################################################################################################
########################################################################################################
#################################################BARAJAS################################################
########################################################################################################
########################################################################################################
load("../Mejor modelo final/barajas.RData")

#Lectura:
fichero <- "barajas.xlsx"
datos <- read.xlsx(fichero) %>% 
  mutate(Mes = seq(from = as.Date("2006-01-01"), to = as.Date("2021-07-01"), by = 'month')) %>%
  as_tbl_time(index = Mes) %>% rename(Precio = Precio.m2) %>% filter(!is.na(Precio))

#Predicciones:
calibration_table <- MejorModelo %>%
  modeltime_calibrate(datos)
predicciones <- calibration_table %>% 
  modeltime_forecast(h = "24 months", actual_data = datos) 
calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  plot_modeltime_forecast(.interactive = FALSE)

#Escritura:
predicciones <- calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  rename(Fecha = .index, Valor = .value, ConfLow = .conf_lo, ConfUp = .conf_hi,
         TipoValor = .key) %>% select(c(Fecha, TipoValor, Valor, ConfLow, ConfUp)) %>%
  mutate(Valor = round(Valor))
write.xlsx(predicciones, "../Predicciones/barajas.xlsx")


########################################################################################################
########################################################################################################
##############################################CARABANCHEL###############################################
########################################################################################################
########################################################################################################
load("../Mejor modelo final/carabanchel.RData")

#Lectura:
fichero <- "carabanchel.xlsx"
datos <- read.xlsx(fichero) %>% 
  mutate(Mes = seq(from = as.Date("2006-01-01"), to = as.Date("2021-07-01"), by = 'month')) %>%
  as_tbl_time(index = Mes) %>% rename(Precio = Precio.m2) %>% filter(!is.na(Precio))

#Predicciones:
calibration_table <- MejorModelo %>%
  modeltime_calibrate(datos)
predicciones <- calibration_table %>% 
  modeltime_forecast(h = "24 months", actual_data = datos) 
calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  plot_modeltime_forecast(.interactive = FALSE)

#Escritura:
predicciones <- calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  rename(Fecha = .index, Valor = .value, ConfLow = .conf_lo, ConfUp = .conf_hi,
         TipoValor = .key) %>% select(c(Fecha, TipoValor, Valor, ConfLow, ConfUp)) %>%
  mutate(Valor = round(Valor))
write.xlsx(predicciones, "../Predicciones/carabanchel.xlsx")


########################################################################################################
########################################################################################################
#################################################CENTRO#################################################
########################################################################################################
########################################################################################################
load("../Mejor modelo final/centro.RData")

#Lectura:
fichero <- "centro.xlsx"
datos <- read.xlsx(fichero) %>% 
  mutate(Mes = seq(from = as.Date("2006-01-01"), to = as.Date("2021-07-01"), by = 'month')) %>%
  as_tbl_time(index = Mes) %>% rename(Precio = Precio.m2) %>% filter(!is.na(Precio))

#Predicciones:
calibration_table <- MejorModelo %>%
  modeltime_calibrate(datos)
predicciones <- calibration_table %>% 
  modeltime_forecast(h = "24 months", actual_data = datos) 
calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  plot_modeltime_forecast(.interactive = FALSE)

#Escritura:
predicciones <- calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  rename(Fecha = .index, Valor = .value, ConfLow = .conf_lo, ConfUp = .conf_hi,
         TipoValor = .key) %>% select(c(Fecha, TipoValor, Valor, ConfLow, ConfUp)) %>%
  mutate(Valor = round(Valor))
write.xlsx(predicciones, "../Predicciones/centro.xlsx")



########################################################################################################
########################################################################################################
###############################################CHAMARTIN################################################
########################################################################################################
########################################################################################################
load("../Mejor modelo final/chamartin.RData")

#Lectura:
fichero <- "chamartin.xlsx"
datos <- read.xlsx(fichero) %>% 
  mutate(Mes = seq(from = as.Date("2006-01-01"), to = as.Date("2021-07-01"), by = 'month')) %>%
  as_tbl_time(index = Mes) %>% rename(Precio = Precio.m2) %>% filter(!is.na(Precio))

#Predicciones:
calibration_table <- MejorModelo %>%
  modeltime_calibrate(datos)
predicciones <- calibration_table %>% 
  modeltime_forecast(h = "24 months", actual_data = datos) 
calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  plot_modeltime_forecast(.interactive = FALSE)

#Escritura:
predicciones <- calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  rename(Fecha = .index, Valor = .value, ConfLow = .conf_lo, ConfUp = .conf_hi,
         TipoValor = .key) %>% select(c(Fecha, TipoValor, Valor, ConfLow, ConfUp)) %>%
  mutate(Valor = round(Valor))
write.xlsx(predicciones, "../Predicciones/chamartin.xlsx")


########################################################################################################
########################################################################################################
################################################CHAMBERI################################################
########################################################################################################
########################################################################################################
load("../Mejor modelo final/chamberi.RData")

#Lectura:
fichero <- "chamberi.xlsx"
datos <- read.xlsx(fichero) %>% 
  mutate(Mes = seq(from = as.Date("2006-01-01"), to = as.Date("2021-07-01"), by = 'month')) %>%
  as_tbl_time(index = Mes) %>% rename(Precio = Precio.m2) %>% filter(!is.na(Precio))

#Predicciones:
calibration_table <- MejorModelo %>%
  modeltime_calibrate(datos)
predicciones <- calibration_table %>% 
  modeltime_forecast(h = "24 months", actual_data = datos) 
calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  plot_modeltime_forecast(.interactive = FALSE)

#Escritura:
predicciones <- calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  rename(Fecha = .index, Valor = .value, ConfLow = .conf_lo, ConfUp = .conf_hi,
         TipoValor = .key) %>% select(c(Fecha, TipoValor, Valor, ConfLow, ConfUp)) %>%
  mutate(Valor = round(Valor))
write.xlsx(predicciones, "../Predicciones/chamberi.xlsx")


########################################################################################################
########################################################################################################
#############################################CIUDAD LINEAL##############################################
########################################################################################################
########################################################################################################
load("../Mejor modelo final/ciudadlineal.RData")

#Lectura:
fichero <- "ciudadlineal.xlsx"
datos <- read.xlsx(fichero) %>% 
  mutate(Mes = seq(from = as.Date("2006-01-01"), to = as.Date("2021-07-01"), by = 'month')) %>%
  as_tbl_time(index = Mes) %>% rename(Precio = Precio.m2) %>% filter(!is.na(Precio))

#Predicciones:
calibration_table <- MejorModelo %>%
  modeltime_calibrate(datos)
predicciones <- calibration_table %>% 
  modeltime_forecast(h = "24 months", actual_data = datos) 
calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  plot_modeltime_forecast(.interactive = FALSE)

#Escritura:
predicciones <- calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  rename(Fecha = .index, Valor = .value, ConfLow = .conf_lo, ConfUp = .conf_hi,
         TipoValor = .key) %>% select(c(Fecha, TipoValor, Valor, ConfLow, ConfUp)) %>%
  mutate(Valor = round(Valor))
write.xlsx(predicciones, "../Predicciones/ciudadlineal.xlsx")


########################################################################################################
########################################################################################################
##############################################FUENCARRAL################################################
########################################################################################################
########################################################################################################
load("../Mejor modelo final/fuencarral.RData")

#Lectura:
fichero <- "fuencarral.xlsx"
datos <- read.xlsx(fichero) %>% 
  mutate(Mes = seq(from = as.Date("2006-01-01"), to = as.Date("2021-07-01"), by = 'month')) %>%
  as_tbl_time(index = Mes) %>% rename(Precio = Precio.m2) %>% filter(!is.na(Precio))

#Predicciones:
calibration_table <- MejorModelo %>%
  modeltime_calibrate(datos)
predicciones <- calibration_table %>% 
  modeltime_forecast(h = "24 months", actual_data = datos) 
calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  plot_modeltime_forecast(.interactive = FALSE)

#Escritura:
predicciones <- calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  rename(Fecha = .index, Valor = .value, ConfLow = .conf_lo, ConfUp = .conf_hi,
         TipoValor = .key) %>% select(c(Fecha, TipoValor, Valor, ConfLow, ConfUp)) %>%
  mutate(Valor = round(Valor))
write.xlsx(predicciones, "../Predicciones/fuencarral.xlsx")


########################################################################################################
########################################################################################################
##############################################HORTALEZA#################################################
########################################################################################################
########################################################################################################
load("../Mejor modelo final/hortaleza.RData")

#Lectura:
fichero <- "hortaleza.xlsx"
datos <- read.xlsx(fichero) %>% 
  mutate(Mes = seq(from = as.Date("2006-01-01"), to = as.Date("2021-07-01"), by = 'month')) %>%
  as_tbl_time(index = Mes) %>% rename(Precio = Precio.m2) %>% filter(!is.na(Precio))

#Predicciones:
calibration_table <- MejorModelo %>%
  modeltime_calibrate(datos)
predicciones <- calibration_table %>% 
  modeltime_forecast(h = "24 months", actual_data = datos) 
calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  plot_modeltime_forecast(.interactive = FALSE)

#Escritura:
predicciones <- calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  rename(Fecha = .index, Valor = .value, ConfLow = .conf_lo, ConfUp = .conf_hi,
         TipoValor = .key) %>% select(c(Fecha, TipoValor, Valor, ConfLow, ConfUp)) %>%
  mutate(Valor = round(Valor))
write.xlsx(predicciones, "../Predicciones/hortaleza.xlsx")

########################################################################################################
########################################################################################################
################################################LATINA#################################################
########################################################################################################
########################################################################################################
load("../Mejor modelo final/latina.RData")

#Lectura:
fichero <- "latina.xlsx"
datos <- read.xlsx(fichero) %>% 
  mutate(Mes = seq(from = as.Date("2006-01-01"), to = as.Date("2021-07-01"), by = 'month')) %>%
  as_tbl_time(index = Mes) %>% rename(Precio = Precio.m2) %>% filter(!is.na(Precio))

#Predicciones:
calibration_table <- MejorModelo %>%
  modeltime_calibrate(datos)
predicciones <- calibration_table %>% 
  modeltime_forecast(h = "24 months", actual_data = datos) 
calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  plot_modeltime_forecast(.interactive = FALSE)

#Escritura:
predicciones <- calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  rename(Fecha = .index, Valor = .value, ConfLow = .conf_lo, ConfUp = .conf_hi,
         TipoValor = .key) %>% select(c(Fecha, TipoValor, Valor, ConfLow, ConfUp)) %>%
  mutate(Valor = round(Valor))
write.xlsx(predicciones, "../Predicciones/latina.xlsx")


########################################################################################################
########################################################################################################
################################################MADRID##################################################
########################################################################################################
########################################################################################################
load("../Mejor modelo final/madrid.RData")

#Lectura:
fichero <- "madrid.xlsx"
datos <- read.xlsx(fichero) %>% 
  mutate(Mes = seq(from = as.Date("2006-01-01"), to = as.Date("2021-07-01"), by = 'month')) %>%
  as_tbl_time(index = Mes) %>% rename(Precio = Precio.m2) %>% filter(!is.na(Precio))

#Predicciones:
calibration_table <- MejorModelo %>%
  modeltime_calibrate(datos)
predicciones <- calibration_table %>% 
  modeltime_forecast(h = "24 months", actual_data = datos) 
calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  plot_modeltime_forecast(.interactive = FALSE)

#Escritura:
predicciones <- calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  rename(Fecha = .index, Valor = .value, ConfLow = .conf_lo, ConfUp = .conf_hi,
         TipoValor = .key) %>% select(c(Fecha, TipoValor, Valor, ConfLow, ConfUp)) %>%
  mutate(Valor = round(Valor))
write.xlsx(predicciones, "../Predicciones/madrid.xlsx")



########################################################################################################
########################################################################################################
###############################################MONCLOA##################################################
########################################################################################################
########################################################################################################
load("../Mejor modelo final/moncloa.RData")

#Lectura:
fichero <- "moncloa.xlsx"
datos <- read.xlsx(fichero) %>% 
  mutate(Mes = seq(from = as.Date("2006-01-01"), to = as.Date("2021-07-01"), by = 'month')) %>%
  as_tbl_time(index = Mes) %>% rename(Precio = Precio.m2) %>% filter(!is.na(Precio))

#Predicciones:
calibration_table <- MejorModelo %>%
  modeltime_calibrate(datos)
predicciones <- calibration_table %>% 
  modeltime_forecast(h = "24 months", actual_data = datos) 
calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  plot_modeltime_forecast(.interactive = FALSE)


#Escritura:
predicciones <- calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  rename(Fecha = .index, Valor = .value, ConfLow = .conf_lo, ConfUp = .conf_hi,
         TipoValor = .key) %>% select(c(Fecha, TipoValor, Valor, ConfLow, ConfUp)) %>%
  mutate(Valor = round(Valor))
write.xlsx(predicciones, "../Predicciones/moncloa.xlsx")



########################################################################################################
########################################################################################################
#############################################MORATALAZ##################################################
########################################################################################################
########################################################################################################
load("../Mejor modelo final/moratalaz.RData")

#Lectura:
fichero <- "moratalaz.xlsx"
datos <- read.xlsx(fichero) %>% 
  mutate(Mes = seq(from = as.Date("2006-01-01"), to = as.Date("2021-07-01"), by = 'month')) %>%
  as_tbl_time(index = Mes) %>% rename(Precio = Precio.m2) %>% filter(!is.na(Precio))

#Predicciones:
calibration_table <- MejorModelo %>%
  modeltime_calibrate(datos)
predicciones <- calibration_table %>% 
  modeltime_forecast(h = "24 months", actual_data = datos) 
calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  plot_modeltime_forecast(.interactive = FALSE)


#Escritura:
predicciones <- calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  rename(Fecha = .index, Valor = .value, ConfLow = .conf_lo, ConfUp = .conf_hi,
         TipoValor = .key) %>% select(c(Fecha, TipoValor, Valor, ConfLow, ConfUp)) %>%
  mutate(Valor = round(Valor))
write.xlsx(predicciones, "../Predicciones/moratalaz.xlsx")



########################################################################################################
########################################################################################################
#############################################PUENTEVALLECAS#############################################
########################################################################################################
########################################################################################################
load("../Mejor modelo final/puentedevallecas.RData")

#Lectura:
fichero <- "puentedevallecas.xlsx"
datos <- read.xlsx(fichero) %>% 
  mutate(Mes = seq(from = as.Date("2006-01-01"), to = as.Date("2021-07-01"), by = 'month')) %>%
  as_tbl_time(index = Mes) %>% rename(Precio = Precio.m2) %>% filter(!is.na(Precio))

#Predicciones:
calibration_table <- MejorModelo %>%
  modeltime_calibrate(datos)
predicciones <- calibration_table %>% 
  modeltime_forecast(h = "24 months", actual_data = datos) 
calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  plot_modeltime_forecast(.interactive = FALSE)

#Escritura:
predicciones <- calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  rename(Fecha = .index, Valor = .value, ConfLow = .conf_lo, ConfUp = .conf_hi,
         TipoValor = .key) %>% select(c(Fecha, TipoValor, Valor, ConfLow, ConfUp)) %>%
  mutate(Valor = round(Valor))
write.xlsx(predicciones, "../Predicciones/puentedevallecas.xlsx")


########################################################################################################
########################################################################################################
###################################################RETIRO###############################################
########################################################################################################
########################################################################################################
load("../Mejor modelo final/retiro.RData")

#Lectura:
fichero <- "retiro.xlsx"
datos <- read.xlsx(fichero) %>% 
  mutate(Mes = seq(from = as.Date("2006-01-01"), to = as.Date("2021-07-01"), by = 'month')) %>%
  as_tbl_time(index = Mes) %>% rename(Precio = Precio.m2) %>% filter(!is.na(Precio))

#Predicciones:
calibration_table <- MejorModelo %>%
  modeltime_calibrate(datos)
predicciones <- calibration_table %>% 
  modeltime_forecast(h = "24 months", actual_data = datos) 
calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  plot_modeltime_forecast(.interactive = FALSE)

#Escritura:
predicciones <- calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  rename(Fecha = .index, Valor = .value, ConfLow = .conf_lo, ConfUp = .conf_hi,
         TipoValor = .key) %>% select(c(Fecha, TipoValor, Valor, ConfLow, ConfUp)) %>%
  mutate(Valor = round(Valor))
write.xlsx(predicciones, "../Predicciones/retiro.xlsx")



########################################################################################################
########################################################################################################
################################################SALAMANCA###############################################
########################################################################################################
########################################################################################################
load("../Mejor modelo final/salamanca.RData")

#Lectura:
fichero <- "salamanca.xlsx"
datos <- read.xlsx(fichero) %>% 
  mutate(Mes = seq(from = as.Date("2006-01-01"), to = as.Date("2021-07-01"), by = 'month')) %>%
  as_tbl_time(index = Mes) %>% rename(Precio = Precio.m2) %>% filter(!is.na(Precio))

#Predicciones:
calibration_table <- MejorModelo %>%
  modeltime_calibrate(datos)
predicciones <- calibration_table %>% 
  modeltime_forecast(h = "24 months", actual_data = datos) 
calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  plot_modeltime_forecast(.interactive = FALSE)

#Escritura:
predicciones <- calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  rename(Fecha = .index, Valor = .value, ConfLow = .conf_lo, ConfUp = .conf_hi,
         TipoValor = .key) %>% select(c(Fecha, TipoValor, Valor, ConfLow, ConfUp)) %>%
  mutate(Valor = round(Valor))
write.xlsx(predicciones, "../Predicciones/salamanca.xlsx")


########################################################################################################
########################################################################################################
#################################################SANBLAS################################################
########################################################################################################
########################################################################################################
load("../Mejor modelo final/sanblas.RData")

#Lectura:
fichero <- "sanblas.xlsx"
datos <- read.xlsx(fichero) %>% 
  mutate(Mes = seq(from = as.Date("2006-01-01"), to = as.Date("2021-07-01"), by = 'month')) %>%
  as_tbl_time(index = Mes) %>% rename(Precio = Precio.m2) %>% filter(!is.na(Precio))

#Predicciones:
calibration_table <- MejorModelo %>%
  modeltime_calibrate(datos)
predicciones <- calibration_table %>% 
  modeltime_forecast(h = "24 months", actual_data = datos) 
calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  plot_modeltime_forecast(.interactive = FALSE)

#Escritura:
predicciones <- calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  rename(Fecha = .index, Valor = .value, ConfLow = .conf_lo, ConfUp = .conf_hi,
         TipoValor = .key) %>% select(c(Fecha, TipoValor, Valor, ConfLow, ConfUp)) %>%
  mutate(Valor = round(Valor))
write.xlsx(predicciones, "../Predicciones/sanblas.xlsx")



########################################################################################################
########################################################################################################
##################################################TETUAN################################################
########################################################################################################
########################################################################################################
load("../Mejor modelo final/tetuan.RData")

#Lectura:
fichero <- "tetuan.xlsx"
datos <- read.xlsx(fichero) %>% 
  mutate(Mes = seq(from = as.Date("2006-01-01"), to = as.Date("2021-07-01"), by = 'month')) %>%
  as_tbl_time(index = Mes) %>% rename(Precio = Precio.m2) %>% filter(!is.na(Precio))

#Predicciones:
calibration_table <- MejorModelo %>%
  modeltime_calibrate(datos)
predicciones <- calibration_table %>% 
  modeltime_forecast(h = "24 months", actual_data = datos) 
calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  plot_modeltime_forecast(.interactive = FALSE)

#Escritura:
predicciones <- calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  rename(Fecha = .index, Valor = .value, ConfLow = .conf_lo, ConfUp = .conf_hi,
         TipoValor = .key) %>% select(c(Fecha, TipoValor, Valor, ConfLow, ConfUp)) %>%
  mutate(Valor = round(Valor))
write.xlsx(predicciones, "../Predicciones/tetuan.xlsx")


########################################################################################################
########################################################################################################
###################################################USERA################################################
########################################################################################################
########################################################################################################
load("../Mejor modelo final/usera.RData")

#Lectura:
fichero <- "usera.xlsx"
datos <- read.xlsx(fichero) %>% 
  mutate(Mes = seq(from = as.Date("2006-01-01"), to = as.Date("2021-07-01"), by = 'month')) %>%
  as_tbl_time(index = Mes) %>% rename(Precio = Precio.m2) %>% filter(!is.na(Precio))

#Predicciones:
calibration_table <- MejorModelo %>%
  modeltime_calibrate(datos)
predicciones <- calibration_table %>% 
  modeltime_forecast(h = "24 months", actual_data = datos) 
calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  plot_modeltime_forecast(.interactive = FALSE)


#Escritura:
predicciones <- calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  rename(Fecha = .index, Valor = .value, ConfLow = .conf_lo, ConfUp = .conf_hi,
         TipoValor = .key) %>% select(c(Fecha, TipoValor, Valor, ConfLow, ConfUp)) %>%
  mutate(Valor = round(Valor))
write.xlsx(predicciones, "../Predicciones/usera.xlsx")




########################################################################################################
########################################################################################################
#################################################VICALVARO##############################################
########################################################################################################
########################################################################################################
load("../Mejor modelo final/vicalvaro.RData")

#Lectura:
fichero <- "vicalvaro.xlsx"
datos <- read.xlsx(fichero) %>% 
  mutate(Mes = seq(from = as.Date("2006-01-01"), to = as.Date("2021-07-01"), by = 'month')) %>%
  as_tbl_time(index = Mes) %>% rename(Precio = Precio.m2) %>% filter(!is.na(Precio))

#Predicciones:
calibration_table <- MejorModelo %>%
  modeltime_calibrate(datos)
predicciones <- calibration_table %>% 
  modeltime_forecast(h = "24 months", actual_data = datos) 
calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  plot_modeltime_forecast(.interactive = FALSE)

#Escritura:
predicciones <- calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  rename(Fecha = .index, Valor = .value, ConfLow = .conf_lo, ConfUp = .conf_hi,
         TipoValor = .key) %>% select(c(Fecha, TipoValor, Valor, ConfLow, ConfUp)) %>%
  mutate(Valor = round(Valor))
write.xlsx(predicciones, "../Predicciones/vicalvaro.xlsx")



########################################################################################################
########################################################################################################
#############################################VILLADEVALLECAS############################################
########################################################################################################
########################################################################################################
load("../Mejor modelo final/villadevallecas.RData")

#Lectura:
fichero <- "villadevallecas.xlsx"
datos <- read.xlsx(fichero) %>% 
  mutate(Mes = seq(from = as.Date("2006-01-01"), to = as.Date("2021-07-01"), by = 'month')) %>%
  as_tbl_time(index = Mes) %>% rename(Precio = Precio.m2) %>% filter(!is.na(Precio))

#Predicciones:
calibration_table <- MejorModelo %>%
  modeltime_calibrate(datos)
predicciones <- calibration_table %>% 
  modeltime_forecast(h = "24 months", actual_data = datos) 
calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  plot_modeltime_forecast(.interactive = FALSE)

#Escritura:
predicciones <- calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  rename(Fecha = .index, Valor = .value, ConfLow = .conf_lo, ConfUp = .conf_hi,
         TipoValor = .key) %>% select(c(Fecha, TipoValor, Valor, ConfLow, ConfUp)) %>%
  mutate(Valor = round(Valor))
write.xlsx(predicciones, "../Predicciones/villadevallecas.xlsx")




########################################################################################################
########################################################################################################
################################################VILLAVERDE##############################################
########################################################################################################
########################################################################################################
load("../Mejor modelo final/villaverde.RData")

#Lectura:
fichero <- "villaverde.xlsx"
datos <- read.xlsx(fichero) %>% 
  mutate(Mes = seq(from = as.Date("2006-01-01"), to = as.Date("2021-07-01"), by = 'month')) %>%
  as_tbl_time(index = Mes) %>% rename(Precio = Precio.m2) %>% filter(!is.na(Precio))

#Predicciones:
calibration_table <- MejorModelo %>%
  modeltime_calibrate(datos)
predicciones <- calibration_table %>% 
  modeltime_forecast(h = "24 months", actual_data = datos) 
calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  plot_modeltime_forecast(.interactive = FALSE)


#Escritura:
predicciones <- calibration_table %>%
  modeltime_forecast(h = "24 months", actual_data = datos) %>%
  rename(Fecha = .index, Valor = .value, ConfLow = .conf_lo, ConfUp = .conf_hi,
         TipoValor = .key) %>% select(c(Fecha, TipoValor, Valor, ConfLow, ConfUp)) %>%
  mutate(Valor = round(Valor))
write.xlsx(predicciones, "../Predicciones/villaverde.xlsx")

