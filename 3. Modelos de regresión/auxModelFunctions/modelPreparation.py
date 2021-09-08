def createCenteredGridSearch(rndGrid, porcentageStep=0.3, maxRange=2, expandBool=False):
    """
    Recibe como argumento un diccinario que contienen una serie de hiperparametros y crea un grid search centrado en los
    mismos. Los valores de estos hiperparámetros deben de ser o booleanos o enteros. No admite listas en los hiperparámetros,
    puesto que va a crear una lista a partir de ellos. Los valores booleanos se mantienen si el parámetro expandBool = false.
    (recomendado).

    :param rndGrid: Diccionario que se utilizará para crear un grid especifico centrado.
    :param porcentageStep: Porcentage del valor del hiperparámetro que se utilizará como separación entre los valores. A mayor valor,
                           menor número de posibilidades en el hiperparámetro
    :param maxRange: Numero de veces que es mayor el rango maximo respecto al valor del hiperparámtro.
    :param expandBool: Valor que permite expacreateCenteredGridSearchndir los booleanos (como consecuencia se multiplica por 2 las combinaciones del grid)

    :return: Devuelve un diccionario con los posibles hiperparámetros para el grid que se usará en el grid search.
    """
    maxRange = int(maxRange)
    gridSearchGrid = {}
    for key in rndGrid.keys():
        gridSearchGrid[key] = []
    for key, value in rndGrid.items():
        if type(value) is bool:
            if expandBool:
                gridSearchGrid[key] = [True, False]
            else:
                gridSearchGrid[key].append(value)
        else:  # Es un número
            if type(value) is not str and (value is not None):
                if value > 10:
                    gridSearchGrid[key] = list(range(value, value * maxRange, int(value * porcentageStep)))
                elif value > 2:
                    gridSearchGrid[key] = list(range(value - 2, value + 2))
                elif value in [1, 2]:
                    gridSearchGrid[key] = list(range(1, value + 1))
                else:  # Evaluacion de la parte decimal.
                    gridSearchGrid[key] = [(value - (value * 0.1)), value, (value - (value * 0.1))]
            else:
                gridSearchGrid[key].append(value)
    return gridSearchGrid


def shortCenteredGridSearch(rndGrid: dict, pctg_variation=0.15, expandBool=False):
    """
    Recibe como argumento un diccionario que contienen una serie de hiper-parámetros y crea un grid search centrado en los
    mismos. Los valores de estos hiper-parámetros deben de ser o booleanos, decimales, enteros o string. No admite listas en los hiper-parámetros,
    puesto que va a crear una lista a partir de ellos. Los valores booleanos se mantienen si el parámetro expandBool = false.
    (recomendado).
    :param rndGrid: Diccionario que se utilizará para crear un grid especifico centrado.
    :param expandBool: Valor que permite expandir los booleanos (como consecuencia se multiplica por 2 las combinaciones del grid)
    :param pctg_variation: porcentaje que se van a desviar del centro los hiper-parámetros generados.
    :return: Devuelve un diccionario con los posibles hiper-parámetros para el grid que se usará en el grid search.
    """
    gridSearchGrid = {}

    for key in rndGrid.keys():
        gridSearchGrid[key] = []
    for key, value in rndGrid.items():
        if type(value) is bool:
            if expandBool:
                gridSearchGrid[key] = [True, False]
            else:
                gridSearchGrid[key].append(value)
        else:  # Es un número
            if type(value) is not str and (value is not None):
                deviation = value * pctg_variation
                if type(value) is int:
                    if int(deviation) < 0:  # Caso de variaciones pequeñas para hiper-parámetros enteros
                        if value > 1:
                            gridSearchGrid[key] = [(value - 1), value, (value + 1)]
                        else:
                            gridSearchGrid[key] = [value, (value + 1), (value + 2)]
                    else:
                        gridSearchGrid[key] = [(value - int(deviation)), value, (value + int(deviation))]
                else:
                    gridSearchGrid[key] = [(value - deviation), value, (value + deviation)]
            else:
                gridSearchGrid[key].append(value)
    return gridSearchGrid
