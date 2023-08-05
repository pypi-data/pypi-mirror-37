"""

Decorators to extend feature computation function (based on 2d numpy array) to
 support different types of input, such as pandas dataframe, csv file, 1d numpy
 array, and to extend feature computation as a standalone script to compute
windowed values directly

Author: Qu Tang

Date: 07/10/2018

"""
import pandas as pd
import numpy as np


def apply_on_accelerometer_dataframe(func):
    def wrapper_func(df, *args, **kwargs):
        result = df.copy(deep=True)
        X = result.iloc[:, 1:].values
        result.iloc[:, 1:] = func(X, *args, **kwargs)
        return result
    return wrapper_func
