from ...libs.data_formatting import validator
from ...libs.data_formatting import formatter
import numpy as np


def _check_input(X):
    if not validator.is_xyz_inertial(X):
        raise ValueError(
            'Input numpy array must be a 3 axis sensor')


def flip_and_swap(X, x_flip, y_flip, z_flip):
    _check_input(X)
    X = formatter.as_float64(X)
    X_clone = np.copy(X)
    x = np.copy(X_clone[:, 0])
    y = np.copy(X_clone[:, 1])
    z = np.copy(X_clone[:, 2])
    x_flip = x_flip.lower()
    y_flip = y_flip.lower()
    z_flip = z_flip.lower()
    if x_flip == 'x':
        X_clone[:, 0] = x
    elif x_flip == '-x':
        X_clone[:, 0] = -x
    elif x_flip == 'y':
        X_clone[:, 0] = y
    elif x_flip == '-y':
        X_clone[:, 0] = -y
    elif x_flip == 'z':
        X_clone[:, 0] = z
    elif x_flip == '-z':
        X_clone[:, 0] = -z

    if y_flip == 'x':
        X_clone[:, 1] = x
    elif y_flip == '-x':
        X_clone[:, 1] = -x
    elif y_flip == 'y':
        X_clone[:, 1] = y
    elif y_flip == '-y':
        X_clone[:, 1] = -y
    elif y_flip == 'z':
        X_clone[:, 1] = z
    elif y_flip == '-z':
        X_clone[:, 1] = -z

    if z_flip == 'x':
        X_clone[:, 2] = x
    elif z_flip == '-x':
        X_clone[:, 2] = -x
    elif z_flip == 'y':
        X_clone[:, 2] = y
    elif z_flip == '-y':
        X_clone[:, 2] = -y
    elif z_flip == 'z':
        X_clone[:, 2] = z
    elif z_flip == '-z':
        X_clone[:, 2] = -z

    return X_clone
