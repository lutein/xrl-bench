# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd


class AUM:
    def __init__(self, environment, **kwargs):
        """
        Class for evaluating the Accuracy on Unimportant feature Masked by zero padding [AUM].

        Parameters:
        -----------
        environment : object
            The environment used for evaluating XRL methods.
        """
        self.environment = environment

    def evaluate(self, X, y, feature_weights, k=5):
        """
        Evaluate the performance of XRL methods using AUM metric.

        Parameters:
        -----------
        X : pandas.DataFrame or numpy.ndarray
            The input data.
        y : pandas.Series or numpy.ndarray
            The true labels for the input data.
        feature_weights : numpy.ndarray
            The feature weights computed using an XRL method.
        k : int, optional (default=5)
            The number of top feature to mask.

        Returns:
        --------
        accuracy : float
            The mean accuracy on unimportant feature masked by zero padding.

        """
        # Check inputs
        if not isinstance(X, (pd.DataFrame, np.ndarray)):
            raise TypeError("X must be a pandas.DataFrame or a numpy.ndarray")
        if not isinstance(y, (np.ndarray, pd.Series)):
            raise TypeError("y must be a numpy.ndarray or pandas.Series")
        X = X.values if isinstance(X, pd.DataFrame) else X
        y = y.values if isinstance(y, pd.Series) else y
        if len(np.array(feature_weights).shape) == 3:
            feature_weights = [feature_weights[i, :, int(y)] for i in range(len(feature_weights))]
        elif len(np.array(feature_weights).shape) != 2:
            raise ValueError("Invalid shape for feature_weights.")
        weights_ranks = [np.argsort(feature_weights[i]) for i in range(len(feature_weights))]
        masked_X = X.copy()
        for i in range(X.shape[0]):
            masked_X[i][weights_ranks[i][:k]] = 0
        y_pred = self.environment.agent.act(masked_X)
        accuracy = np.mean(y_pred == y)
        return accuracy

        # accuracy = []
        # if len(np.array(feature_weights).shape) == 3:
        #     feature_weights = [feature_weights[i, :, int(y[i])] for i in range(len(feature_weights))]
        # weights_ranks = [np.argsort(feature_weights[i]) for i in range(len(feature_weights))]
        # # if len(np.array(feature_weights).shape) == 2:
        # #     weights_ranks = [np.argsort(feature_weights[i]) for i in range(len(feature_weights))]
        # # elif len(np.array(feature_weights).shape) == 3:
        # #     weights_ranks = [np.argsort(feature_weights[i, :, int(y[i])]) for i in range(len(feature_weights))]
        # for i in range(X.shape[0]):
        #     X[i][weights_ranks[i][:-k]] = 0
        #     action = self.dataset.agent.act(X[i])
        #     if action == y[i]:
        #         accuracy.append(1)
        #     else:
        #         accuracy.append(0)
        # return np.mean(accuracy)
