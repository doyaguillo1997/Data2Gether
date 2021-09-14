def deleteColumns(column_pattern, dataframe):
    """
    Esta función permite eliminar aquellas columnas que contengan una palabra o un patron en el nombre de sus columnas,
    de manera que podamos eliminar de golpe columnas creadas de manera automatica por error como por ejemplo la columna
    unnamed
    :param dataframe: Dataframe sobre el que queremos borrar las columnas.
    :param column_pattern: cadena que contiene el nombre de la/s columna/columnas a eliminar.
    :return: Devuelve el dataframe con la/s columna/s eliminada/s.
    """

    df = dataframe.copy()
    columns = list(df.columns)
    deletedColumns = list()
    if column_pattern is list:
        for col in columns:
            for word in column_pattern:
                if word in col:
                    deletedColumns.append(col)
    else:
        for col in columns:
            if column_pattern in col:
                deletedColumns.append(col)

    dataframe.drop(deletedColumns, 1)
    return df


def orderColumns(df_or, key):
    """
    Funcion para ordenar las columnas de un dataframe, en funcion de su nombre.

    :param df_or: dataframe en el que queremos ordenar las columnas
    :param key: funcion que se aplica a cada elemento antes de ordenarlo. Se recomienda str.lower
    :return:
    """

    cols = list(df_or.columns)
    cols.sort(reverse=True, key=key)
    df_or = df_or.reindex(columns=cols)
    return df_or


def isInside(circle_x, circle_y, x, y, rad_km):
    """
    Funcion que calcula si un punto esta dentro de un circulo o no

    :param circle_x: coordenada x del centro del circulo sobre el que se observa si esta dentro o no el punto
    :param circle_y: coordenada y del centro del circulo sobre el que se observa si esta dentro o no el punto
    :param x: coordenada x sobre la que se calcula si el punto esta dentro del circulo
    :param y: coordenada y sobre la que se calcula si el punto esta dentro del circulo
    :rad_km: radio del círculo en kilómetros
    :return: Devuelve True si el punto está dentro del radio definido. False en caso de que no lo este.
    """
    rad = rad_km * 60 / 6371  # Mejor Radio = 1000m o 1200m, corr con el precio de 0.55 (se ha probado rad = 800,1000,1200,1400)
    if (x - circle_x) ** 2 + (y - circle_y) ** 2 <= rad ** 2:
        return True
    else:
        return False


def longitudCategorias(df, obj):
    """
    Obtiene un diccionario con la representacion de cada categoria en la variable

    :param df: dataframe sobre el que se tienen los datos
    :param obj: columna del dataframe.
    :return: diccionario con las categorias como clave y la cantidad de veces que aparece como valor
    """
    cuenta = df[obj].value_counts()
    variables = list(cuenta.index)
    cantidad = cuenta.to_list()
    datos = dict(zip(variables, cantidad))

    return datos


def isNumber(value):
    """
    Recibe una cadena y evalúa si es un numero o no. Evalúa números enteros
    :param value: Cadena a introducir
    :return: True en caso de que sea un número
    """
    import re
    if re.fullmatch(r'(-|)[0-9]+', value, 0) is not None:
        return True
    else:
        return False


def flatList(t):
    """
    Convierte una lista de lista en una lista plana.
    :param t:  Lista que contienen listas anidadas
    :return:  Lista plana
    """
    return [item for sublist in t for item in sublist]


def isNan(value):
    """
    Por equivalencia np.NaN != np.NaN por lo tanto comparando el valor consigo mismo obtendremos siempre true, salvo en
    los casos que tengamos NaN.

    :param value: Valor a validar
    :return:  True en caso de que el valor introducido sea un nulo o np.NaN.
    """
    if value == value:
        return False
    else:
        return True