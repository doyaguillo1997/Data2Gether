from sklearn.base import BaseEstimator, TransformerMixin
from generalFunctions import isNumber, isNan


class LowerTransformer(BaseEstimator, TransformerMixin):
    """
    Clase que devuelve la distancia a un punto específico según latitud/longitud.
    MAGNITUDES: Distancias en <km> y latitudes/longitudes en <minutos>.
    LÓGICA: Se suma el cuadrado de la diferencias de las latitudes/longitudes y se obtiene la raiz cuadrada.
            El resultado se obtiene en <minutos>, por lo que se devide entre 60 para transformarlo en <grados> y
            se multiplica por 6370 (radio de la Tierra en <km>) para pasarlo a <km>.

    :param X: DataFrame sobre el que se van a realizar los cambios.
    :param new_columns: Nombre con el se crea la nueva columna.
    :param transformed_columns: Columnas de donde obtener los datos. Las magnitudes de estas columnas deben de ser en
                                "minutos".
    :param origin: Punto de referencia para obtener las distancias.
    :return: Devuelve el DataFrame modificado con la nueva columna, que contiene la distancia al punto seleccionado en
             kilometros.
    """

    def __init__(self):
        super().__init__()

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X_ = X.copy()
        str_features = X_.select_dtypes(include='object').columns  # Columnas con str
        for column in str_features:
            X_[column].apply(lambda floor: floor if isNumber(str(floor)) or isNan(floor) else str.lower(floor))
        return X_

