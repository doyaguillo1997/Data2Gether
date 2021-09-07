from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import unidecode as udc
import scipy

class CustomOneHotEncoder(BaseEstimator, TransformerMixin):
    """
    Clase que convierte a dummies las variables categóricas de un dataFrame. Permite eliminar
    las dummies creadas según su representación.

    :param X: DataFrame sobre el que se van a realizar los cambios.
    :param categorical_columns: Lista de las variables categóricas para transformar.
    :param features_not_drop: Lista de las variables categóricas que se transforman pero de las que no
                              queremos eliminar las columnas resultantes según su representación.
    :param threshold: Valor númerico entre 0 y 1 que indica el punto de corte para eliminar las dummies
                      según representación. Se corta según el % de 0 que contiene la columna. Todas las
                      columnas con un % de 0s mayor que el threshold indicado son eliminadas.
    :param sparse_matrix: Bool. Si es True el transformador devuelve una SparseMatrix. Por defecto
                          False y devuelve un DataFrame
    :return: Devuelve el DataFrame o SparseMatrix modificado con las nuevas dummies.
    """

    def __init__(self, categorical_columns, features_not_drop, threshold, sparse_matrix = False):
        super().__init__()
        self.categorical_columns = categorical_columns
        self.threshold = threshold
        self.features_not_drop = features_not_drop
        self.sparse_matrix = sparse_matrix
        self.columns_to_drop_ = list()

    def fit(self, X, y=None):
        X_ = X.copy()
        
        # Dummies para las categóricas
        X__ = pd.get_dummies(X_, drop_first = False)

        # Se marcan las columnas que se van a borrar
        for feat in self.categorical_columns:
            X__.rename(columns=lambda x: 
                             udc.unidecode(x.replace(feat, 'oneHotEncoder_' + feat)),
                             inplace = True)
        
        for feat in self.features_not_drop:
            X__.rename(columns=lambda x: 
                             udc.unidecode(x.replace('oneHotEncoder_' + feat, 'oneHotEncoderX_' + feat)),
                             inplace = True)
            
        # Se seleccionan las columnas del OneHot con representación 'threshold'
        for feat in X__.columns:
            try:
                if ((X__[feat].value_counts(normalize = True)[0] > self.threshold) & ('oneHotEncoder_' in feat)):
                    self.columns_to_drop_.append(feat)
            except:
                pass
        
        return self

    def transform(self, X, y=None):
        X_ = X.copy()        

        X__ = pd.get_dummies(X_, drop_first = False)
        for feat in self.categorical_columns:
            X__.rename(columns=lambda x: 
                             udc.unidecode(x.replace(feat, 'oneHotEncoder_' + feat)),
                             inplace = True)
        
        # Se eliminan las columnas seleccionadas del dataframe
        for col in self.columns_to_drop_:
            try:
                X__.drop(columns= col, inplace = True)
            except:
                pass

        # Se eliminan caracteres de los column_names no admitidos por el modelo
        X__.rename(columns=lambda x: udc.unidecode(x.replace("]", ")")), inplace = True)
        
        if self.sparse_matrix:
            X__ = scipy.sparse.csr_matrix(X__.values)
        
        return X__