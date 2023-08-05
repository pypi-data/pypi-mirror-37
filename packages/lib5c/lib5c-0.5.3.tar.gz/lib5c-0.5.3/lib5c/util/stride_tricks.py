"""
Module for sliding window views and other stride tricks.
"""


import numpy as np


def sliding_window_view(x, shape, subok=False, readonly=True):
    """
    Creates sliding window views of the N dimensional array with the given
    window shape. Window slides across each dimension of ``x`` and extract
    subsets of `x` at any window position.

    Implementation taken from https://github.com/numpy/numpy/pull/10771 while
    waiting for it to be merged.

    Parameters
    ----------
    x : array_like
        Array to create sliding window views of.
    shape : sequence of int
        The shape of the window. Must have same length as the number of input
        array dimensions.
    subok : bool, optional
        If True, then sub-classes will be passed-through, otherwise the returned
        array will be forced to be a base-class array (default).
    readonly : bool, optional
        If set to True, the returned array will always be readonly view.
        Otherwise it will return writable copies (see Notes).

    Returns
    -------
    view : np.ndarray
        Sliding window views (or copies) of `x`.
        view.shape = x.shape - shape + 1

    See also
    --------
    as_strided: Create a view into the array with the given shape and strides.
    broadcast_to: broadcast an array to a given shape.

    Notes
    -----
    ``sliding_window_view`` create sliding window views of the N dimensions
    array with the given window shape and its implementation based on
    ``as_strided``. Please note that if readonly set to True, views are
    returned, not copies of array. In this case, write operations could be
    unpredictable, so the returned views are readonly. Bear in mind that
    returned copies (readonly=False) will take more memory than the original
    array, due to overlapping windows. For some cases there may be more
    efficient approaches to calculate transformations across multi-dimensional
    arrays, for instance `scipy.signal.fftconvolve`, where combining the
    iterating step with the calculation itself while storing partial results
    can result in significant speedups.

    Examples
    --------
    >>> i, j = np.ogrid[:3,:4]
    >>> x = 10*i + j
    >>> shape = (2,2)
    >>> np.lib.stride_tricks.sliding_window_view(x, shape)
    array([[[[ 0,  1],
             [10, 11]],
            [[ 1,  2],
             [11, 12]],
            [[ 2,  3],
             [12, 13]]],
           [[[10, 11],
             [20, 21]],
            [[11, 12],
             [21, 22]],
            [[12, 13],
             [22, 23]]]])
    """
    # first convert input to array, possibly keeping subclass
    x = np.array(x, copy=False, subok=subok)

    try:
        shape = np.array(shape, np.int)
    except:
        raise TypeError('`shape` must be a sequence of integer')
    else:
        if shape.ndim > 1:
            raise ValueError('`shape` must be one-dimensional sequence of '
                             'integer')
        if len(x.shape) != len(shape):
            raise ValueError("`shape` length doesn't match with input array "
                             "dimensions")
        if np.any(shape <= 0):
            raise ValueError('`shape` cannot contain non-positive value')

    o = np.array(x.shape) - shape + 1  # output shape
    if np.any(o <= 0):
        raise ValueError('window shape cannot larger than input array shape')

    if type(readonly) != bool:
        raise TypeError('readonly must be a boolean')

    strides = x.strides
    view_strides = strides

    view_shape = np.concatenate((o, shape), axis=0)
    view_strides = np.concatenate((view_strides, strides), axis=0)
    view = np.lib.stride_tricks.as_strided(x, view_shape, view_strides,
                                           subok=subok, writeable=not readonly)

    if not readonly:
        return view.copy()
    else:
        return view
