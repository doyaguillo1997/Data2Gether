from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

class SizeMeanEncoder(BaseEstimator, TransformerMixin):
    """
    Clase que devuelve el tamaño medio en <m2> según distrito/barrio.

    :param X: DataFrame sobre el que se van a realizar los cambios.
    :param new_columns: Nombre con el se crea la nueva columna.
    :param transformed_columns: Columnas de donde obtener los datos.
    :param group: Columna donde hacer el groupBy.
    :param mean_values_: Promedio de la columna "transformed_columns" tras agrupar por la columna "group"
    :return: Devuelve el DataFrame modificado con la nueva columna.
    """

    def __init__(self, new_columns, transformed_columns, group):
        super().__init__()
        self.new_columns = new_columns
        self.transformed_columns = transformed_columns
        self.group = group
        self.mean_values_ = None

    def fit(self, X, y=None):
        X_ = X.copy()
        self.mean_values_ = X_.groupby(self.group)[self.transformed_columns].mean().rename(self.new_columns, inplace = True)
        
        return self

    def transform(self, X, y=None):
        X_ = X.copy()        
        X_ = pd.merge(X_, self.mean_values_, how='left', left_on=self.group, right_on=self.group)

        return X_