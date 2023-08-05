
from sklearn.base import BaseEstimator, TransformerMixin
from .luriegold_func import luriegold


class LurieGold(BaseEstimator, TransformerMixin):
    def __init__(self):
        """No settings required"""

    def fit(self, X, y=None):
        """Do nothing and return the estimator unchanged"""
        return self

    def transform(self, X):
        C, _, _ = luriegold(X)
        return C
