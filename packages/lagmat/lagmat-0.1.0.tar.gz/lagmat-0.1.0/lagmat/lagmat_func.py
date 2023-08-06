import numpy as np


def lagmat(A, lags=[], order='F'):
    """Create array with time-lagged copies of the features/variables

    Parameters
    ----------
    A : np.ndarray
        Dataset. One column for each features/variables, and one
        row for each example/observation at a certain time step.

    lags : list, tuple
        Definition what time lags the copies of A should have.

    order : str
        (Optional) Default 'F'

    Assumptions
    -----------
    * It's a time-homogenous time series (that's why there is
        no time index)
    * Features/Variables are ordered from the oldest example/observation
        (1st row) to the latest example (last row)
    * Any Missing Value treatment have been done previously.

    """
    if lags:
        # correct dimensions
        if len(A.shape) is 1:
            A = A.reshape(-1, 1)

        # number of colums and lags
        n_rows, n_cols = A.shape
        n_lags = len(lags)

        # allocate memory
        B = np.empty(
            shape=(n_rows, n_cols * n_lags),
            order=order,
            dtype=float)
        B[:] = np.nan

        # Copy lagged columns of A into B
        for i, l in enumerate(lags):
            # target columns of B
            j = i * n_cols
            k = j + n_cols  # (i+1) * ncols
            # number rows of A
            nl = n_rows - l
            # Copy
            B[l:, j:k] = A[:nl, :]

        return B
    else:
        return None
