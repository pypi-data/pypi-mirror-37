import numpy as np


def apply_over_subwins(X, func, subwins=None, subwin_samples=None, **kwargs):
    if subwins is not None:
        win_length = int(np.floor(X.shape[0] / subwins))
    elif subwin_samples is not None:
        win_length = subwin_samples
        subwins = int(np.floor(X.shape[0] / subwin_samples))
    else:
        subwins = 1
        win_length = X.shape[0]
    start_index = np.ceil((X.shape[0] % subwins) / 2)
    result = []
    for i in range(0, subwins):
        indices = int(start_index) + np.array(range(
            i * win_length,
            (i + 1) * win_length
        ))
        subwin_X = X[indices, :]
        result.append(func(subwin_X, **kwargs))
    return result
