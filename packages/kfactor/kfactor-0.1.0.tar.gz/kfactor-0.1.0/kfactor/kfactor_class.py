from sklearn.base import BaseEstimator, TransformerMixin
from .kfactor_func import kfactor


class KFactor(BaseEstimator, TransformerMixin):
    def __init__(self, k=2, algorithm='COBYLA'):
        """No settings required"""
        self.k = k
        self.algorithm = algorithm

    def fit(self, X, y=None):
        """Do nothing and return the estimator unchanged"""
        return self

    def transform(self, X):
        C, _, _, _, _ = kfactor(X, k=self.k, algorithm=self.algorithm)
        return C
