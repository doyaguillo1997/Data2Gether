from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

class RangeEncoder(BaseEstimator, TransformerMixin):
    """
    Clase que divide en rangos de valores la columna a transformar.

    :param X: DataFrame sobre el que se van a realizar los cambios.
    :param new_columns: Nombre con el se crea la nueva columna FE.
    :param transformed_columns: Columnas de donde obtener los datos.
    :param bins: Número de divisiones.
    :param kwargs: Argumentos extras para la función cut de pandas.
    :return: Devuelve el DataFrame modificado con la nueva columna.
    """

    def __init__(self, new_columns, transformed_columns, bins, **kwargs):
        super().__init__()
        self.new_columns = new_columns
        self.transformed_columns = transformed_columns
        self.bins = bins
        self.kwargs = kwargs
        self.min_ = None
        self.max_ = None

    def fit(self, X, y=None):
        self.min_ = X[self.transformed_columns].min() - X[self.transformed_columns].std()
        self.max_ = X[self.transformed_columns].max() + X[self.transformed_columns].std()

        return self

    def transform(self, X, y=None):
        X_ = X.copy()
        X_[self.transformed_columns] = X_[self.transformed_columns].apply(lambda value: self.min_
                                                                          if value < self.min_ else value)\
                                                                   .apply(lambda value: self.max_
                                                                          if value > self.max_ else value)

        X_[self.new_columns] = pd.cut(X_[self.transformed_columns], self.bins, **self.kwargs)
        
        return X_