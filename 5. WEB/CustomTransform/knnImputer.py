from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
from sklearn.impute import KNNImputer

class CustomKNNImputer(BaseEstimator, TransformerMixin):
    """
    Clase que imputa los nulos de las variables numéricas mediante el KNNImputer de Sklearn.
    (KNNImputer doc: https://scikit-learn.org/stable/modules/generated/sklearn.impute.KNNImputer.html)

    :param X: DataFrame sobre el que se van a realizar los cambios.
    :param n_neighbors: Parámetro propio del KNNImputer de Sklearn.
    :param weights: Parámetro propio del KNNImputer de Sklearn.
    :return: Devuelve el DataFrame con los nulos imputados en las variables numéricas.
    """

    def __init__(self, n_neighbors, weights):
        super().__init__()
        self.model_ = None
        self.n_neighbors = n_neighbors
        self.weights = weights
        self.num_features_ = None

    def fit(self, X, y=None):
        X_ = X.copy()
        self.num_features_ = X_.select_dtypes(include = 'number').columns
        
        imputer = KNNImputer(n_neighbors = self.n_neighbors, weights = self.weights)
        self.model_ = imputer.fit(X_[self.num_features_])
        
        return self

    def transform(self, X, y=None):
        X_ = X.copy()
        X_[self.num_features_] = self.model_.transform(X_[self.num_features_])        
        
        return X_
