# Models
from sklearn import *
from sklearn.ensemble import *

# Transformers

from CustomTransform import DistanceEncoder
from CustomTransform import SizeMeanEncoder
from CustomTransform import RangeEncoder
from CustomTransform import RangeOtherEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer


# Model Evaluation

from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import KFold, cross_val_score
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import GridSearchCV
from auxModelFunctions import modelEvaluate, shortCenteredGridSearch, modelsDirectory
import pickle

# Utility
from tqdm.notebook import tqdm_notebook


def __numberOfModels(grid: dict):
    """
    Dado un grid para los diferentes métodos calcula el numero de combinaciones posibles para componer un modelo
    :param grid: Diccionario con los hiperparámetros.
    :return: nº de combinaciones
    """
    n_model = 1
    for param, options in grid.items():
        n_model = n_model*len(options)

    return n_model


def __randomFactoryModels(models: dict, X, y):
    """
    Crea una serie de modelos aleatorios entorno a grids aleatorias sobre los modelos, para que sean utilizables las mejores
    sobre
    :param models: Diccionario que contiene el nombre del modelo, la instancia del mismo y el grid que define sus
                   iteraciones aleatorias. La clave del diccionario debe de ser el nombre del modelo que se quiere ajustar
                   y la clave una lista de dos elementos, el primero un pipeline de sklearn con los transformadores y el
                   segundo un grid con los parametros que se desea aleatorizar. El formato del grid tiene que se un
                   diccionario, con la claves el parámetro a modificar y las claves una lista de los valores que se van
                   a utilizar en el grid search.
    :param X : Features para entrenar los modelos
    :param y : Labels variable objetivo del modelo
    :return: un diccionario que contiene le nombre del modelo, el objeto y el grid que ha utilizado.
    """

    bestModels = {}
    for modelName, modelParams in tqdm_notebook(models.items(), desc="Probando algoritmos"):
        # modelParams[0] -> Contiene el pipeline utilizado
        # modelParams[1] -> Contiene el grid usado para el randomGridSearch
        print("probando " + str(__numberOfModels(modelParams[1])) + " combinaciones aleatorias de " + modelName)
        auxModels = RandomizedSearchCV(estimator=modelParams[0], param_distributions=modelParams[1],
                                       n_iter=10, cv=5, verbose=1, random_state=42, n_jobs=-1, scoring='neg_mean_absolute_percentage_error')
        auxModels.fit(X, y)
        bestModels[modelName] = [modelParams[0], auxModels.best_estimator_, auxModels.best_params_, auxModels.best_score_]
        pickle.dump(bestModels[modelName][1], open('./models/random/'+modelName+"_random", 'wb'))
    return bestModels


def __bestFactoryModels(models: dict, X, y):
    """
    Crea una serie de modelos centrados entorno a grids aleatorias de manera que se profundice más en aquellos que han obtenido
    un mejor score con los grid aleatorios.
    :param models: Listado de modelos
    :param X : Features para entrenar los modelos
    :param y : Labels variable objetivo del modelo
    :return: un diccionario que contiene le nombre del modelo, el objeto y el grid que ha utilizado.
    """

    bestModels = {}
    for modelName, modelParams in tqdm_notebook(models.items(), desc="Centrando los mejores modelos aleatorios"):
        # modelParams[0] -> Contiene el pipeline utilizado
        # modelParams[2] -> Contiene el grid usado para el gridSearch
        param_grid = shortCenteredGridSearch(modelParams[2])
        # print("probando " + str(__numberOfModels(modelParams[2])) + modelName + " centrados")
        auxModels = GridSearchCV(estimator=modelParams[0], param_grid=param_grid,
                                 cv=5, verbose=1, n_jobs=-1, scoring='neg_mean_absolute_percentage_error')
        auxModels.fit(X, y)
        bestModels[modelName] = [auxModels.best_estimator_, auxModels.best_params_, auxModels.best_score_]
        pickle.dump(bestModels[modelName][0], open("./models/centered/best_"+modelName, 'wb'))

    return bestModels


def bestModel(models: dict, X, y, test_X, test_y):
    """
    Crea una serie de modelos aleatorios entorno a grids aleatorias sobre los modelos, para que sean utilizables las mejores
    sobre
    :param models: Listado de modelos con su pipeline y su grid search aleatorio
    :param X : Features para entrenar los modelos.
    :param y : Labels variable objetivo del modelo.
    :param test_X: Features para evaluar el modelo.
    :param test_y: Labels objetivo para evaluar el modelo.
    :return: un diccionario que contiene le nombre del modelo, el objeto y el grid que ha utilizado.
    """

    modelsDirectory()
    
    bestModels = __bestFactoryModels(__randomFactoryModels(models, X, y), X, y)

    auxMetric = 0
    bstModel = []
    name = ""
    for name, model in bestModels.items():
        if modelEvaluate(model[0], test_X, test_y) > auxMetric:
            bstModel = model
            name = name
    pickle.dump(bstModel, open("./models/GOATModel_" + name, 'wb'))
    return bstModel