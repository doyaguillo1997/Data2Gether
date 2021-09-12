########################################################################################################
########################################################################################################
###############################################RANDOM FOREST############################################
########################################################################################################
########################################################################################################
#Funcion para obtener el mejor Random Forest acorde a la serie temporal

mejor_random_forest <- function(fichero, ini_datos, fin_datos, meses_valid){
  require(openxlsx)
  require(dplyr)
  require(tibbletime)
  require(timetk) 
  require(tidymodels)
  require(modeltime)
  
  #Leo el fichero y lo paso a formato tbl_time
  datos <- read.xlsx(fichero) %>% 
    mutate(Mes = seq(from = as.Date(ini_datos), to = as.Date(fin_datos), by = 'month')) %>%
    as_tbl_time(index = Mes) %>% rename(Precio = Precio.m2) %>% filter(!is.na(Precio))
  
  #Especifico los meses de test
  splits <- datos %>%
    time_series_split(assess = paste(meses_valid, "months"), cumulative = TRUE)
  
  #Adapto el data frame para el ML:
  recipe_spec <- recipe(Precio ~ Mes, training(splits)) %>%
    step_timeseries_signature(Mes) %>%
    step_rm(contains("am.pm"), contains("hour"), contains("minute"),
            contains("second"), contains("xts"), contains("day"),
            contains("week"), Mes_year.iso) %>%
    step_fourier(Mes, period = 12, K = 3)
  
  
  #Creo la rejilla de parametros a probar
  mtry <- c(2, 4, 7)
  trees <- c(500, 1000, 1500)
  min_n <- c(2, 4, 10, 15, 30)
  parm_grid <- crossing(mtry, trees, min_n)
  
  #Ajusto y guardo el error de los distintos modelos:
  error <- c()
  for(i in 1:nrow(parm_grid)){
    model_spec_rf <- rand_forest(trees = parm_grid$trees[i], min_n = parm_grid$min_n[i], 
                                 mtry = parm_grid$mtry[i]) %>%
      set_engine("randomForest")
    error <- c(error, workflow() %>%
                 add_model(model_spec_rf) %>%
                 add_recipe(recipe_spec %>% step_rm(Mes)) %>%
                 fit(training(splits)) %>%
                 modeltime_calibrate(testing(splits)) %>%
                 modeltime_accuracy() %>% select(rmse))
  }
  
  
  #Obtengo los parametros asociados al modelo con menor rmse
  parm_grid[which.min(error), ] %>% as.data.frame()
}


########################################################################################################
########################################################################################################
###################################################XGBOOST##############################################
########################################################################################################
########################################################################################################
#Funcion para obtener el mejor XGBoost acorde a la serie temporal

mejor_xgboost <- function(fichero, ini_datos, fin_datos, meses_valid){
  require(openxlsx)
  require(dplyr)
  require(tibbletime)
  require(timetk) 
  require(tidymodels)
  require(modeltime)
  
  #Leo el fichero y lo paso a formato tbl_time
  datos <- read.xlsx(fichero) %>% 
    mutate(Mes = seq(from = as.Date(ini_datos), to = as.Date(fin_datos), by = 'month')) %>%
    as_tbl_time(index = Mes) %>% rename(Precio = Precio.m2) %>% filter(!is.na(Precio))
  
  #Especifico los meses de test
  splits <- datos %>%
    time_series_split(assess = paste(meses_valid, "months"), cumulative = TRUE)
  
  #Adapto el data frame para el ML:
  recipe_spec <- recipe(Precio ~ Mes, training(splits)) %>%
    step_timeseries_signature(Mes) %>%
    step_rm(contains("am.pm"), contains("hour"), contains("minute"),
            contains("second"), contains("xts"), contains("day"),
            contains("week"), Mes_year.iso) %>%
    step_fourier(Mes, period = 12, K = 3) %>%
    step_dummy(all_nominal())
  
  
  #Creo la rejilla de parametros a probar
  mtry <- c(2, 4, 7)
  trees <- c(1000, 800, 1500)
  min_n <- c(2, 4, 10, 15, 30)
  learn_rate <- c(0.0001, 0.001, 0.01, 0.1)
  parm_grid <- crossing(mtry, trees, min_n, learn_rate)
  
  #Ajusto y guardo el error de los distintos modelos:
  error <- c()
  for(i in 1:nrow(parm_grid)){
    model_spec_rf <- boost_tree(trees = parm_grid$trees[i], min_n = parm_grid$min_n[i],
                                mtry = parm_grid$mtry[i], learn_rate = parm_grid$learn_rate[i]) %>%
      set_engine("xgboost")
    error <- c(error, workflow() %>%
                 add_model(model_spec_rf) %>%
                 add_recipe(recipe_spec %>% step_rm(Mes)) %>%
                 fit(training(splits)) %>%
                 modeltime_calibrate(testing(splits)) %>%
                 modeltime_accuracy() %>% select(rmse))
  }
  
  
  #Obtengo los parametros asociados al modelo con menor rmse
  parm_grid[which.min(error), ] %>% as.data.frame()
  
}


########################################################################################################
########################################################################################################
###################################################GLMNET###############################################
########################################################################################################
########################################################################################################
#Funcion para obtener el mejor modelo lineal acorde a la serie temporal

mejor_glmnet <- function(fichero, ini_datos, fin_datos, meses_valid){
  require(openxlsx)
  require(dplyr)
  require(tibbletime)
  require(timetk) 
  require(tidymodels)
  require(modeltime)
  
  #Leo el fichero y lo paso a formato tbl_time
  datos <- read.xlsx(fichero) %>% 
    mutate(Mes = seq(from = as.Date(ini_datos), to = as.Date(fin_datos), by = 'month')) %>%
    as_tbl_time(index = Mes) %>% rename(Precio = Precio.m2) %>% filter(!is.na(Precio))
  
  #Especifico los meses de test
  splits <- datos %>%
    time_series_split(assess = paste(meses_valid, "months"), cumulative = TRUE)
  
  #Adapto el data frame para el ML:
  recipe_spec <- recipe(Precio ~ Mes, training(splits)) %>%
    step_timeseries_signature(Mes) %>%
    step_rm(contains("am.pm"), contains("hour"), contains("minute"),
            contains("second"), contains("xts"), contains("day"),
            contains("week"), Mes_year.iso) %>%
    step_fourier(Mes, period = 12, K = 3) %>%
    step_dummy(all_nominal())
  
  
  #Creo la rejilla de parametros a probar
  penalty <- c(0.1, 0.5, 1, 3, 5)
  mixture <- c(0.0001, 0.001, 0.01, 0.1, 0.3, 0.5)
  parm_grid <- crossing(penalty, mixture)
  
  #Ajusto y guardo el error de los distintos modelos:
  error <- c()
  for(i in 1:nrow(parm_grid)){
    model_spec_rf <- linear_reg(penalty = parm_grid$penalty[i], mixture = parm_grid$mixture[i]) %>%
      set_engine("glmnet")
    error <- c(error, workflow() %>%
                 add_model(model_spec_rf) %>%
                 add_recipe(recipe_spec %>% step_rm(Mes)) %>%
                 fit(training(splits)) %>%
                 modeltime_calibrate(testing(splits)) %>%
                 modeltime_accuracy() %>% select(rmse))
  }
  
  
  #Obtengo los parametros asociados al modelo con menor rmse
  parm_grid[which.min(error), ] %>% as.data.frame()
  
}


########################################################################################################
########################################################################################################
#############################################MEJOR MODELO###############################################
########################################################################################################
########################################################################################################
#Funcion para obtener el mejor modelo de todos los probados en las funciones anteriores 

mejor_modelo <- function(fichero, ini_datos, fin_datos, meses_valid){
  require(openxlsx)
  require(dplyr)
  require(tibbletime)
  require(timetk) 
  require(tidymodels)
  require(modeltime)
  
  #Leo el fichero y lo paso a formato tbl_time
  datos <- read.xlsx(fichero) %>% 
    mutate(Mes = seq(from = as.Date(ini_datos), to = as.Date(fin_datos), by = 'month')) %>%
    as_tbl_time(index = Mes) %>% rename(Precio = Precio.m2) %>% filter(!is.na(Precio))
  
  #Especifico los meses de test
  splits <- datos %>%
    time_series_split(assess = paste(meses_valid, "months"), cumulative = TRUE)
  
  #Adapto el data frame para el ML:
  recipe_spec <- recipe(Precio ~ Mes, training(splits)) %>%
    step_timeseries_signature(Mes) %>%
    step_rm(contains("am.pm"), contains("hour"), contains("minute"),
            contains("second"), contains("xts"), contains("day"),
            contains("week"), Mes_year.iso) %>%
    step_fourier(Mes, period = 12, K = 3) %>%
    step_dummy(all_nominal())
  
  #Saco el ARIMA:
  model_fit_arima <- arima_reg() %>%
    set_engine("auto_arima") %>%
    fit(Precio ~ Mes, training(splits))
  
  #Saco el Random Forest:
  param_rf <- mejor_random_forest(fichero, ini_datos, fin_datos, meses_valid)
  model_spec_rf <- rand_forest(trees = param_rf$trees, min_n = param_rf$min_n,
                               mtry = param_rf$mtry) %>%
    set_engine("randomForest")
  model_fit_rf <- workflow() %>%
    add_model(model_spec_rf) %>%
    add_recipe(recipe_spec %>% step_rm(Mes)) %>%
    fit(training(splits))
  
  #Saco el XGBoost:
  param_xgb <- mejor_xgboost(fichero, ini_datos, fin_datos, meses_valid)
  model_spec_xgb <- boost_tree(trees = param_xgb$trees, min_n = param_xgb$min_n,
                               mtry = param_xgb$mtry, learn_rate = param_xgb$learn_rate) %>%
    set_engine("xgboost")
  model_fit_xgb <- workflow() %>%
    add_model(model_spec_xgb) %>%
    add_recipe(recipe_spec %>% step_rm(Mes)) %>%
    fit(training(splits))
  
  #Saco la Red Neuronal:
  param_glmn <- mejor_glmnet(fichero, ini_datos, fin_datos, meses_valid)
  model_spec_glmnet <- linear_reg(penalty = param_glmn$penalty, mixture = param_glmn$mixture) %>%
    set_engine("glmnet")
  model_fit_glmn <- workflow() %>%
    add_model(model_spec_glmnet) %>%
    add_recipe(recipe_spec %>% step_rm(Mes)) %>%
    fit(training(splits))
  
  #Guardo el mejor modelo de cada tipo:
  MejoresModelos <- list(arima = model_fit_arima, rf= model_fit_rf, 
                         xgb = model_fit_xgb, glmn = model_fit_glmn)
  MejoresModelos
  
}


########################################################################################################
########################################################################################################
#######################################MEJOR MODELO CON ENSAMBLADO######################################
########################################################################################################
########################################################################################################
#Funcion para, dado un modelo de cada algoritmo, obtener el ensamblado que mejor se adapta a la serie

mejor_ensamblado <- function(fichero, ini_datos, fin_datos, meses_valid){
  require(openxlsx)
  require(dplyr)
  require(tibbletime)
  require(timetk) 
  require(tidymodels)
  require(modeltime)
  require(modeltime.ensemble)
  
  #Lectura modelos:
  load(paste0("../Mejores modelos de cada tipo/", substr(fichero, 1, nchar(fichero) - 5), ".RData"))
  model_fit_arima <- MejorModelo$arima
  model_fit_rf <- MejorModelo$rf
  model_fit_xgb <- MejorModelo$xgb
  model_fit_glmn <- MejorModelo$glmn
  
  #Lectura datos:
  datos <- read.xlsx(fichero) %>% 
    mutate(Mes = seq(from = as.Date(ini_datos), to = as.Date(fin_datos), by = 'month')) %>%
    as_tbl_time(index = Mes) %>% rename(Precio = Precio.m2) %>% filter(!is.na(Precio))
  splits <- datos %>%
    time_series_split(assess = paste(meses_valid, "months"), cumulative = TRUE)
  
  #Ensamblados (de media, con todos los pesos iguales):
  ensamblados <- list(modeltime_table(model_fit_arima, model_fit_glmn) %>%  
                        ensemble_average(type = "mean"),
                      modeltime_table(model_fit_arima, model_fit_rf) %>%  
                        ensemble_average(type = "mean"),
                      modeltime_table(model_fit_arima, model_fit_xgb) %>%  
                        ensemble_average(type = "mean"),
                      modeltime_table(model_fit_glmn, model_fit_rf) %>%  
                        ensemble_average(type = "mean"),
                      modeltime_table(model_fit_glmn, model_fit_xgb) %>%  
                        ensemble_average(type = "mean"),
                      modeltime_table(model_fit_rf, model_fit_xgb) %>%  
                        ensemble_average(type = "mean"),
                      modeltime_table(model_fit_arima, model_fit_glmn, model_fit_rf) %>%  
                        ensemble_average(type = "mean"),
                      modeltime_table(model_fit_arima, model_fit_glmn, model_fit_xgb) %>%  
                        ensemble_average(type = "mean"),
                      modeltime_table(model_fit_arima, model_fit_rf, model_fit_xgb) %>%  
                        ensemble_average(type = "mean"),
                      modeltime_table(model_fit_glmn, model_fit_rf, model_fit_xgb) %>%  
                        ensemble_average(type = "mean"),
                      modeltime_table(model_fit_arima, model_fit_glmn, model_fit_rf, model_fit_xgb) %>%  
                        ensemble_average(type = "mean"))
  
  #Resultados:
  error_ensamblados <- c()
  for(ensamble_n in 1:length(ensamblados)){
    error_ensamblados <- c(error_ensamblados, 
                           ensamblados[[ensamble_n]] %>% 
                             modeltime_calibrate(new_data = testing(splits), actual_data = datos) %>% 
                             modeltime_accuracy() %>% select(rmse))
  }
  
  #Mejor ensamblado:
  model_fit_ensemble <- ensamblados[[which.min(error_ensamblados)]]
  
  #Guardo todo:
  list(arima = model_fit_arima, rf = model_fit_rf, xgb = model_fit_xgb, 
       glmn = model_fit_glmn, ensemble = model_fit_ensemble)
}




########################################################################################################
########################################################################################################
###############################################MEJOR MODELO#############################################
########################################################################################################
########################################################################################################
#Funcion para seleccionar el mejor modelo, teniendo en cuenta tanto el mejor ensamblado como el mejor
#modelo de cada algoritmo

mejor_modelo_final <- function(fichero, ini_datos, fin_datos, meses_valid){
  require(openxlsx)
  require(dplyr)
  require(tibbletime)
  require(timetk) 
  require(tidymodels)
  require(modeltime)
  require(modeltime.ensemble)
  
  #Lectura modelos:
  load(paste0("../Mejores modelos de cada tipo/", substr(fichero, 1, nchar(fichero) - 5), ".RData"))
  model_fit_arima <- MejorModelos$arima
  model_fit_rf <- MejorModelo$rf
  model_fit_xgb <- MejorModelo$xgb
  model_fit_glmn <- MejorModelo$glmn
  model_fit_ensemble <- MejorModelo$ensemble
  
  #Lectura datos:
  datos <- read.xlsx(fichero) %>% 
    mutate(Mes = seq(from = as.Date(ini_datos), to = as.Date(fin_datos), by = 'month')) %>%
    as_tbl_time(index = Mes) %>% rename(Precio = Precio.m2) %>% filter(!is.na(Precio))
  splits <- datos %>%
    time_series_split(assess = paste(meses_valid, "months"), cumulative = TRUE)
  
  
  #Resultados:
  modelos <- list(model_fit_arima, model_fit_rf, model_fit_xgb,
                  model_fit_glmn, model_fit_ensemble)
  error <- c()
  for(modelo_n in 1:length(modelos)){
    error <- c(error, 
               modelos[[modelo_n]] %>% 
                 modeltime_calibrate(new_data = testing(splits), actual_data = datos) %>% 
                 modeltime_accuracy() %>% select(rmse))
  }
  
  #Mejor modelo:
  modelos[[which.min(error)]]

}
