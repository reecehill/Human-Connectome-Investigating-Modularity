"""
This type stub file was generated by pyright.
"""

from . import _ni_docstrings

__all__ = ['correlate1d', 'convolve1d', 'gaussian_filter1d', 'gaussian_filter', 'prewitt', 'sobel', 'generic_laplace', 'laplace', 'gaussian_laplace', 'generic_gradient_magnitude', 'gaussian_gradient_magnitude', 'correlate', 'convolve', 'uniform_filter1d', 'uniform_filter', 'minimum_filter1d', 'maximum_filter1d', 'minimum_filter', 'maximum_filter', 'rank_filter', 'median_filter', 'percentile_filter', 'generic_filter1d', 'generic_filter']
@_ni_docstrings.docfiller
def correlate1d(input, weights, axis=..., output=..., mode=..., cval=..., origin=...): # -> NDArray[float64] | NDArray[Any]:
    """Calculate a 1-D correlation along the given axis.

    The lines of the array along the given axis are correlated with the
    given weights.

    Parameters
    ----------
    %(input)s
    weights : array
        1-D sequence of numbers.
    %(axis)s
    %(output)s
    %(mode_reflect)s
    %(cval)s
    %(origin)s

    Returns
    -------
    result : ndarray
        Correlation result. Has the same shape as `input`.

    Examples
    --------
    >>> from scipy.ndimage import correlate1d
    >>> correlate1d([2, 8, 0, 4, 1, 9, 9, 0], weights=[1, 3])
    array([ 8, 26,  8, 12,  7, 28, 36,  9])
    """
    ...

@_ni_docstrings.docfiller
def convolve1d(input, weights, axis=..., output=..., mode=..., cval=..., origin=...): # -> NDArray[float64] | NDArray[Any]:
    """Calculate a 1-D convolution along the given axis.

    The lines of the array along the given axis are convolved with the
    given weights.

    Parameters
    ----------
    %(input)s
    weights : ndarray
        1-D sequence of numbers.
    %(axis)s
    %(output)s
    %(mode_reflect)s
    %(cval)s
    %(origin)s

    Returns
    -------
    convolve1d : ndarray
        Convolved array with same shape as input

    Examples
    --------
    >>> from scipy.ndimage import convolve1d
    >>> convolve1d([2, 8, 0, 4, 1, 9, 9, 0], weights=[1, 3])
    array([14, 24,  4, 13, 12, 36, 27,  0])
    """
    ...

@_ni_docstrings.docfiller
def gaussian_filter1d(input, sigma, axis=..., order=..., output=..., mode=..., cval=..., truncate=..., *, radius=...): # -> NDArray[float64] | NDArray[Any]:
    """1-D Gaussian filter.

    Parameters
    ----------
    %(input)s
    sigma : scalar
        standard deviation for Gaussian kernel
    %(axis)s
    order : int, optional
        An order of 0 corresponds to convolution with a Gaussian
        kernel. A positive order corresponds to convolution with
        that derivative of a Gaussian.
    %(output)s
    %(mode_reflect)s
    %(cval)s
    truncate : float, optional
        Truncate the filter at this many standard deviations.
        Default is 4.0.
    radius : None or int, optional
        Radius of the Gaussian kernel. If specified, the size of
        the kernel will be ``2*radius + 1``, and `truncate` is ignored.
        Default is None.

    Returns
    -------
    gaussian_filter1d : ndarray

    Notes
    -----
    The Gaussian kernel will have size ``2*radius + 1`` along each axis. If
    `radius` is None, a default ``radius = round(truncate * sigma)`` will be
    used.

    Examples
    --------
    >>> from scipy.ndimage import gaussian_filter1d
    >>> import numpy as np
    >>> gaussian_filter1d([1.0, 2.0, 3.0, 4.0, 5.0], 1)
    array([ 1.42704095,  2.06782203,  3.        ,  3.93217797,  4.57295905])
    >>> gaussian_filter1d([1.0, 2.0, 3.0, 4.0, 5.0], 4)
    array([ 2.91948343,  2.95023502,  3.        ,  3.04976498,  3.08051657])
    >>> import matplotlib.pyplot as plt
    >>> rng = np.random.default_rng()
    >>> x = rng.standard_normal(101).cumsum()
    >>> y3 = gaussian_filter1d(x, 3)
    >>> y6 = gaussian_filter1d(x, 6)
    >>> plt.plot(x, 'k', label='original data')
    >>> plt.plot(y3, '--', label='filtered, sigma=3')
    >>> plt.plot(y6, ':', label='filtered, sigma=6')
    >>> plt.legend()
    >>> plt.grid()
    >>> plt.show()

    """
    ...

@_ni_docstrings.docfiller
def gaussian_filter(input, sigma, order=..., output=..., mode=..., cval=..., truncate=..., *, radius=..., axes=...): # -> NDArray[float64] | NDArray[Any]:
    """Multidimensional Gaussian filter.

    Parameters
    ----------
    %(input)s
    sigma : scalar or sequence of scalars
        Standard deviation for Gaussian kernel. The standard
        deviations of the Gaussian filter are given for each axis as a
        sequence, or as a single number, in which case it is equal for
        all axes.
    order : int or sequence of ints, optional
        The order of the filter along each axis is given as a sequence
        of integers, or as a single number. An order of 0 corresponds
        to convolution with a Gaussian kernel. A positive order
        corresponds to convolution with that derivative of a Gaussian.
    %(output)s
    %(mode_multiple)s
    %(cval)s
    truncate : float, optional
        Truncate the filter at this many standard deviations.
        Default is 4.0.
    radius : None or int or sequence of ints, optional
        Radius of the Gaussian kernel. The radius are given for each axis
        as a sequence, or as a single number, in which case it is equal
        for all axes. If specified, the size of the kernel along each axis
        will be ``2*radius + 1``, and `truncate` is ignored.
        Default is None.
    axes : tuple of int or None, optional
        If None, `input` is filtered along all axes. Otherwise,
        `input` is filtered along the specified axes. When `axes` is
        specified, any tuples used for `sigma`, `order`, `mode` and/or `radius`
        must match the length of `axes`. The ith entry in any of these tuples
        corresponds to the ith entry in `axes`.

    Returns
    -------
    gaussian_filter : ndarray
        Returned array of same shape as `input`.

    Notes
    -----
    The multidimensional filter is implemented as a sequence of
    1-D convolution filters. The intermediate arrays are
    stored in the same data type as the output. Therefore, for output
    types with a limited precision, the results may be imprecise
    because intermediate results may be stored with insufficient
    precision.

    The Gaussian kernel will have size ``2*radius + 1`` along each axis. If
    `radius` is None, the default ``radius = round(truncate * sigma)`` will be
    used.

    Examples
    --------
    >>> from scipy.ndimage import gaussian_filter
    >>> import numpy as np
    >>> a = np.arange(50, step=2).reshape((5,5))
    >>> a
    array([[ 0,  2,  4,  6,  8],
           [10, 12, 14, 16, 18],
           [20, 22, 24, 26, 28],
           [30, 32, 34, 36, 38],
           [40, 42, 44, 46, 48]])
    >>> gaussian_filter(a, sigma=1)
    array([[ 4,  6,  8,  9, 11],
           [10, 12, 14, 15, 17],
           [20, 22, 24, 25, 27],
           [29, 31, 33, 34, 36],
           [35, 37, 39, 40, 42]])

    >>> from scipy import datasets
    >>> import matplotlib.pyplot as plt
    >>> fig = plt.figure()
    >>> plt.gray()  # show the filtered result in grayscale
    >>> ax1 = fig.add_subplot(121)  # left side
    >>> ax2 = fig.add_subplot(122)  # right side
    >>> ascent = datasets.ascent()
    >>> result = gaussian_filter(ascent, sigma=5)
    >>> ax1.imshow(ascent)
    >>> ax2.imshow(result)
    >>> plt.show()
    """
    ...

@_ni_docstrings.docfiller
def prewitt(input, axis=..., output=..., mode=..., cval=...): # -> NDArray[float64] | NDArray[Any]:
    """Calculate a Prewitt filter.

    Parameters
    ----------
    %(input)s
    %(axis)s
    %(output)s
    %(mode_multiple)s
    %(cval)s

    Returns
    -------
    prewitt : ndarray
        Filtered array. Has the same shape as `input`.

    See Also
    --------
    sobel: Sobel filter

    Notes
    -----
    This function computes the one-dimensional Prewitt filter.
    Horizontal edges are emphasised with the horizontal transform (axis=0),
    vertical edges with the vertical transform (axis=1), and so on for higher
    dimensions. These can be combined to give the magnitude.

    Examples
    --------
    >>> from scipy import ndimage, datasets
    >>> import matplotlib.pyplot as plt
    >>> import numpy as np
    >>> ascent = datasets.ascent()
    >>> prewitt_h = ndimage.prewitt(ascent, axis=0)
    >>> prewitt_v = ndimage.prewitt(ascent, axis=1)
    >>> magnitude = np.sqrt(prewitt_h ** 2 + prewitt_v ** 2)
    >>> magnitude *= 255 / np.max(magnitude) # Normalization
    >>> fig, axes = plt.subplots(2, 2, figsize = (8, 8))
    >>> plt.gray()
    >>> axes[0, 0].imshow(ascent)
    >>> axes[0, 1].imshow(prewitt_h)
    >>> axes[1, 0].imshow(prewitt_v)
    >>> axes[1, 1].imshow(magnitude)
    >>> titles = ["original", "horizontal", "vertical", "magnitude"]
    >>> for i, ax in enumerate(axes.ravel()):
    ...     ax.set_title(titles[i])
    ...     ax.axis("off")
    >>> plt.show()

    """
    ...

@_ni_docstrings.docfiller
def sobel(input, axis=..., output=..., mode=..., cval=...): # -> NDArray[float64] | NDArray[Any]:
    """Calculate a Sobel filter.

    Parameters
    ----------
    %(input)s
    %(axis)s
    %(output)s
    %(mode_multiple)s
    %(cval)s

    Returns
    -------
    sobel : ndarray
        Filtered array. Has the same shape as `input`.

    Notes
    -----
    This function computes the axis-specific Sobel gradient.
    The horizontal edges can be emphasised with the horizontal transform (axis=0),
    the vertical edges with the vertical transform (axis=1) and so on for higher
    dimensions. These can be combined to give the magnitude.

    Examples
    --------
    >>> from scipy import ndimage, datasets
    >>> import matplotlib.pyplot as plt
    >>> import numpy as np
    >>> ascent = datasets.ascent().astype('int32')
    >>> sobel_h = ndimage.sobel(ascent, 0)  # horizontal gradient
    >>> sobel_v = ndimage.sobel(ascent, 1)  # vertical gradient
    >>> magnitude = np.sqrt(sobel_h**2 + sobel_v**2)
    >>> magnitude *= 255.0 / np.max(magnitude)  # normalization
    >>> fig, axs = plt.subplots(2, 2, figsize=(8, 8))
    >>> plt.gray()  # show the filtered result in grayscale
    >>> axs[0, 0].imshow(ascent)
    >>> axs[0, 1].imshow(sobel_h)
    >>> axs[1, 0].imshow(sobel_v)
    >>> axs[1, 1].imshow(magnitude)
    >>> titles = ["original", "horizontal", "vertical", "magnitude"]
    >>> for i, ax in enumerate(axs.ravel()):
    ...     ax.set_title(titles[i])
    ...     ax.axis("off")
    >>> plt.show()

    """
    ...

@_ni_docstrings.docfiller
def generic_laplace(input, derivative2, output=..., mode=..., cval=..., extra_arguments=..., extra_keywords=...): # -> NDArray[float64] | NDArray[Any]:
    """
    N-D Laplace filter using a provided second derivative function.

    Parameters
    ----------
    %(input)s
    derivative2 : callable
        Callable with the following signature::

            derivative2(input, axis, output, mode, cval,
                        *extra_arguments, **extra_keywords)

        See `extra_arguments`, `extra_keywords` below.
    %(output)s
    %(mode_multiple)s
    %(cval)s
    %(extra_keywords)s
    %(extra_arguments)s

    Returns
    -------
    generic_laplace : ndarray
        Filtered array. Has the same shape as `input`.

    """
    ...

@_ni_docstrings.docfiller
def laplace(input, output=..., mode=..., cval=...): # -> NDArray[float64] | NDArray[Any]:
    """N-D Laplace filter based on approximate second derivatives.

    Parameters
    ----------
    %(input)s
    %(output)s
    %(mode_multiple)s
    %(cval)s

    Returns
    -------
    laplace : ndarray
        Filtered array. Has the same shape as `input`.

    Examples
    --------
    >>> from scipy import ndimage, datasets
    >>> import matplotlib.pyplot as plt
    >>> fig = plt.figure()
    >>> plt.gray()  # show the filtered result in grayscale
    >>> ax1 = fig.add_subplot(121)  # left side
    >>> ax2 = fig.add_subplot(122)  # right side
    >>> ascent = datasets.ascent()
    >>> result = ndimage.laplace(ascent)
    >>> ax1.imshow(ascent)
    >>> ax2.imshow(result)
    >>> plt.show()
    """
    ...

@_ni_docstrings.docfiller
def gaussian_laplace(input, sigma, output=..., mode=..., cval=..., **kwargs): # -> NDArray[float64] | NDArray[Any]:
    """Multidimensional Laplace filter using Gaussian second derivatives.

    Parameters
    ----------
    %(input)s
    sigma : scalar or sequence of scalars
        The standard deviations of the Gaussian filter are given for
        each axis as a sequence, or as a single number, in which case
        it is equal for all axes.
    %(output)s
    %(mode_multiple)s
    %(cval)s
    Extra keyword arguments will be passed to gaussian_filter().

    Returns
    -------
    gaussian_laplace : ndarray
        Filtered array. Has the same shape as `input`.

    Examples
    --------
    >>> from scipy import ndimage, datasets
    >>> import matplotlib.pyplot as plt
    >>> ascent = datasets.ascent()

    >>> fig = plt.figure()
    >>> plt.gray()  # show the filtered result in grayscale
    >>> ax1 = fig.add_subplot(121)  # left side
    >>> ax2 = fig.add_subplot(122)  # right side

    >>> result = ndimage.gaussian_laplace(ascent, sigma=1)
    >>> ax1.imshow(result)

    >>> result = ndimage.gaussian_laplace(ascent, sigma=3)
    >>> ax2.imshow(result)
    >>> plt.show()
    """
    ...

@_ni_docstrings.docfiller
def generic_gradient_magnitude(input, derivative, output=..., mode=..., cval=..., extra_arguments=..., extra_keywords=...): # -> NDArray[float64] | NDArray[Any]:
    """Gradient magnitude using a provided gradient function.

    Parameters
    ----------
    %(input)s
    derivative : callable
        Callable with the following signature::

            derivative(input, axis, output, mode, cval,
                       *extra_arguments, **extra_keywords)

        See `extra_arguments`, `extra_keywords` below.
        `derivative` can assume that `input` and `output` are ndarrays.
        Note that the output from `derivative` is modified inplace;
        be careful to copy important inputs before returning them.
    %(output)s
    %(mode_multiple)s
    %(cval)s
    %(extra_keywords)s
    %(extra_arguments)s

    Returns
    -------
    generic_gradient_matnitude : ndarray
        Filtered array. Has the same shape as `input`.

    """
    ...

@_ni_docstrings.docfiller
def gaussian_gradient_magnitude(input, sigma, output=..., mode=..., cval=..., **kwargs): # -> NDArray[float64] | NDArray[Any]:
    """Multidimensional gradient magnitude using Gaussian derivatives.

    Parameters
    ----------
    %(input)s
    sigma : scalar or sequence of scalars
        The standard deviations of the Gaussian filter are given for
        each axis as a sequence, or as a single number, in which case
        it is equal for all axes.
    %(output)s
    %(mode_multiple)s
    %(cval)s
    Extra keyword arguments will be passed to gaussian_filter().

    Returns
    -------
    gaussian_gradient_magnitude : ndarray
        Filtered array. Has the same shape as `input`.

    Examples
    --------
    >>> from scipy import ndimage, datasets
    >>> import matplotlib.pyplot as plt
    >>> fig = plt.figure()
    >>> plt.gray()  # show the filtered result in grayscale
    >>> ax1 = fig.add_subplot(121)  # left side
    >>> ax2 = fig.add_subplot(122)  # right side
    >>> ascent = datasets.ascent()
    >>> result = ndimage.gaussian_gradient_magnitude(ascent, sigma=5)
    >>> ax1.imshow(ascent)
    >>> ax2.imshow(result)
    >>> plt.show()
    """
    ...

@_ni_docstrings.docfiller
def correlate(input, weights, output=..., mode=..., cval=..., origin=...): # -> NDArray[float64] | NDArray[Any]:
    """
    Multidimensional correlation.

    The array is correlated with the given kernel.

    Parameters
    ----------
    %(input)s
    weights : ndarray
        array of weights, same number of dimensions as input
    %(output)s
    %(mode_reflect)s
    %(cval)s
    %(origin_multiple)s

    Returns
    -------
    result : ndarray
        The result of correlation of `input` with `weights`.

    See Also
    --------
    convolve : Convolve an image with a kernel.

    Examples
    --------
    Correlation is the process of moving a filter mask often referred to
    as kernel over the image and computing the sum of products at each location.

    >>> from scipy.ndimage import correlate
    >>> import numpy as np
    >>> input_img = np.arange(25).reshape(5,5)
    >>> print(input_img)
    [[ 0  1  2  3  4]
    [ 5  6  7  8  9]
    [10 11 12 13 14]
    [15 16 17 18 19]
    [20 21 22 23 24]]

    Define a kernel (weights) for correlation. In this example, it is for sum of
    center and up, down, left and right next elements.

    >>> weights = [[0, 1, 0],
    ...            [1, 1, 1],
    ...            [0, 1, 0]]

    We can calculate a correlation result:
    For example, element ``[2,2]`` is ``7 + 11 + 12 + 13 + 17 = 60``.

    >>> correlate(input_img, weights)
    array([[  6,  10,  15,  20,  24],
        [ 26,  30,  35,  40,  44],
        [ 51,  55,  60,  65,  69],
        [ 76,  80,  85,  90,  94],
        [ 96, 100, 105, 110, 114]])

    """
    ...

@_ni_docstrings.docfiller
def convolve(input, weights, output=..., mode=..., cval=..., origin=...): # -> NDArray[float64] | NDArray[Any]:
    """
    Multidimensional convolution.

    The array is convolved with the given kernel.

    Parameters
    ----------
    %(input)s
    weights : array_like
        Array of weights, same number of dimensions as input
    %(output)s
    %(mode_reflect)s
    cval : scalar, optional
        Value to fill past edges of input if `mode` is 'constant'. Default
        is 0.0
    origin : int, optional
        Controls the origin of the input signal, which is where the
        filter is centered to produce the first element of the output.
        Positive values shift the filter to the right, and negative values
        shift the filter to the left. Default is 0.

    Returns
    -------
    result : ndarray
        The result of convolution of `input` with `weights`.

    See Also
    --------
    correlate : Correlate an image with a kernel.

    Notes
    -----
    Each value in result is :math:`C_i = \\sum_j{I_{i+k-j} W_j}`, where
    W is the `weights` kernel,
    j is the N-D spatial index over :math:`W`,
    I is the `input` and k is the coordinate of the center of
    W, specified by `origin` in the input parameters.

    Examples
    --------
    Perhaps the simplest case to understand is ``mode='constant', cval=0.0``,
    because in this case borders (i.e., where the `weights` kernel, centered
    on any one value, extends beyond an edge of `input`) are treated as zeros.

    >>> import numpy as np
    >>> a = np.array([[1, 2, 0, 0],
    ...               [5, 3, 0, 4],
    ...               [0, 0, 0, 7],
    ...               [9, 3, 0, 0]])
    >>> k = np.array([[1,1,1],[1,1,0],[1,0,0]])
    >>> from scipy import ndimage
    >>> ndimage.convolve(a, k, mode='constant', cval=0.0)
    array([[11, 10,  7,  4],
           [10,  3, 11, 11],
           [15, 12, 14,  7],
           [12,  3,  7,  0]])

    Setting ``cval=1.0`` is equivalent to padding the outer edge of `input`
    with 1.0's (and then extracting only the original region of the result).

    >>> ndimage.convolve(a, k, mode='constant', cval=1.0)
    array([[13, 11,  8,  7],
           [11,  3, 11, 14],
           [16, 12, 14, 10],
           [15,  6, 10,  5]])

    With ``mode='reflect'`` (the default), outer values are reflected at the
    edge of `input` to fill in missing values.

    >>> b = np.array([[2, 0, 0],
    ...               [1, 0, 0],
    ...               [0, 0, 0]])
    >>> k = np.array([[0,1,0], [0,1,0], [0,1,0]])
    >>> ndimage.convolve(b, k, mode='reflect')
    array([[5, 0, 0],
           [3, 0, 0],
           [1, 0, 0]])

    This includes diagonally at the corners.

    >>> k = np.array([[1,0,0],[0,1,0],[0,0,1]])
    >>> ndimage.convolve(b, k)
    array([[4, 2, 0],
           [3, 2, 0],
           [1, 1, 0]])

    With ``mode='nearest'``, the single nearest value in to an edge in
    `input` is repeated as many times as needed to match the overlapping
    `weights`.

    >>> c = np.array([[2, 0, 1],
    ...               [1, 0, 0],
    ...               [0, 0, 0]])
    >>> k = np.array([[0, 1, 0],
    ...               [0, 1, 0],
    ...               [0, 1, 0],
    ...               [0, 1, 0],
    ...               [0, 1, 0]])
    >>> ndimage.convolve(c, k, mode='nearest')
    array([[7, 0, 3],
           [5, 0, 2],
           [3, 0, 1]])

    """
    ...

@_ni_docstrings.docfiller
def uniform_filter1d(input, size, axis=..., output=..., mode=..., cval=..., origin=...): # -> NDArray[float64] | NDArray[Any]:
    """Calculate a 1-D uniform filter along the given axis.

    The lines of the array along the given axis are filtered with a
    uniform filter of given size.

    Parameters
    ----------
    %(input)s
    size : int
        length of uniform filter
    %(axis)s
    %(output)s
    %(mode_reflect)s
    %(cval)s
    %(origin)s

    Returns
    -------
    result : ndarray
        Filtered array. Has same shape as `input`.

    Examples
    --------
    >>> from scipy.ndimage import uniform_filter1d
    >>> uniform_filter1d([2, 8, 0, 4, 1, 9, 9, 0], size=3)
    array([4, 3, 4, 1, 4, 6, 6, 3])
    """
    ...

@_ni_docstrings.docfiller
def uniform_filter(input, size=..., output=..., mode=..., cval=..., origin=..., *, axes=...): # -> NDArray[float64] | NDArray[Any]:
    """Multidimensional uniform filter.

    Parameters
    ----------
    %(input)s
    size : int or sequence of ints, optional
        The sizes of the uniform filter are given for each axis as a
        sequence, or as a single number, in which case the size is
        equal for all axes.
    %(output)s
    %(mode_multiple)s
    %(cval)s
    %(origin_multiple)s
    axes : tuple of int or None, optional
        If None, `input` is filtered along all axes. Otherwise,
        `input` is filtered along the specified axes. When `axes` is
        specified, any tuples used for `size`, `origin`, and/or `mode`
        must match the length of `axes`. The ith entry in any of these tuples
        corresponds to the ith entry in `axes`.

    Returns
    -------
    uniform_filter : ndarray
        Filtered array. Has the same shape as `input`.

    Notes
    -----
    The multidimensional filter is implemented as a sequence of
    1-D uniform filters. The intermediate arrays are stored
    in the same data type as the output. Therefore, for output types
    with a limited precision, the results may be imprecise because
    intermediate results may be stored with insufficient precision.

    Examples
    --------
    >>> from scipy import ndimage, datasets
    >>> import matplotlib.pyplot as plt
    >>> fig = plt.figure()
    >>> plt.gray()  # show the filtered result in grayscale
    >>> ax1 = fig.add_subplot(121)  # left side
    >>> ax2 = fig.add_subplot(122)  # right side
    >>> ascent = datasets.ascent()
    >>> result = ndimage.uniform_filter(ascent, size=20)
    >>> ax1.imshow(ascent)
    >>> ax2.imshow(result)
    >>> plt.show()
    """
    ...

@_ni_docstrings.docfiller
def minimum_filter1d(input, size, axis=..., output=..., mode=..., cval=..., origin=...): # -> NDArray[float64] | NDArray[Any]:
    """Calculate a 1-D minimum filter along the given axis.

    The lines of the array along the given axis are filtered with a
    minimum filter of given size.

    Parameters
    ----------
    %(input)s
    size : int
        length along which to calculate 1D minimum
    %(axis)s
    %(output)s
    %(mode_reflect)s
    %(cval)s
    %(origin)s

    Returns
    -------
    result : ndarray.
        Filtered image. Has the same shape as `input`.

    Notes
    -----
    This function implements the MINLIST algorithm [1]_, as described by
    Richard Harter [2]_, and has a guaranteed O(n) performance, `n` being
    the `input` length, regardless of filter size.

    References
    ----------
    .. [1] http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.42.2777
    .. [2] http://www.richardhartersworld.com/cri/2001/slidingmin.html


    Examples
    --------
    >>> from scipy.ndimage import minimum_filter1d
    >>> minimum_filter1d([2, 8, 0, 4, 1, 9, 9, 0], size=3)
    array([2, 0, 0, 0, 1, 1, 0, 0])
    """
    ...

@_ni_docstrings.docfiller
def maximum_filter1d(input, size, axis=..., output=..., mode=..., cval=..., origin=...): # -> NDArray[float64] | NDArray[Any]:
    """Calculate a 1-D maximum filter along the given axis.

    The lines of the array along the given axis are filtered with a
    maximum filter of given size.

    Parameters
    ----------
    %(input)s
    size : int
        Length along which to calculate the 1-D maximum.
    %(axis)s
    %(output)s
    %(mode_reflect)s
    %(cval)s
    %(origin)s

    Returns
    -------
    maximum1d : ndarray, None
        Maximum-filtered array with same shape as input.
        None if `output` is not None

    Notes
    -----
    This function implements the MAXLIST algorithm [1]_, as described by
    Richard Harter [2]_, and has a guaranteed O(n) performance, `n` being
    the `input` length, regardless of filter size.

    References
    ----------
    .. [1] http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.42.2777
    .. [2] http://www.richardhartersworld.com/cri/2001/slidingmin.html

    Examples
    --------
    >>> from scipy.ndimage import maximum_filter1d
    >>> maximum_filter1d([2, 8, 0, 4, 1, 9, 9, 0], size=3)
    array([8, 8, 8, 4, 9, 9, 9, 9])
    """
    ...

@_ni_docstrings.docfiller
def minimum_filter(input, size=..., footprint=..., output=..., mode=..., cval=..., origin=..., *, axes=...):
    """Calculate a multidimensional minimum filter.

    Parameters
    ----------
    %(input)s
    %(size_foot)s
    %(output)s
    %(mode_multiple)s
    %(cval)s
    %(origin_multiple)s
    axes : tuple of int or None, optional
        If None, `input` is filtered along all axes. Otherwise,
        `input` is filtered along the specified axes. When `axes` is
        specified, any tuples used for `size`, `origin`, and/or `mode`
        must match the length of `axes`. The ith entry in any of these tuples
        corresponds to the ith entry in `axes`.

    Returns
    -------
    minimum_filter : ndarray
        Filtered array. Has the same shape as `input`.

    Notes
    -----
    A sequence of modes (one per axis) is only supported when the footprint is
    separable. Otherwise, a single mode string must be provided.

    Examples
    --------
    >>> from scipy import ndimage, datasets
    >>> import matplotlib.pyplot as plt
    >>> fig = plt.figure()
    >>> plt.gray()  # show the filtered result in grayscale
    >>> ax1 = fig.add_subplot(121)  # left side
    >>> ax2 = fig.add_subplot(122)  # right side
    >>> ascent = datasets.ascent()
    >>> result = ndimage.minimum_filter(ascent, size=20)
    >>> ax1.imshow(ascent)
    >>> ax2.imshow(result)
    >>> plt.show()
    """
    ...

@_ni_docstrings.docfiller
def maximum_filter(input, size=..., footprint=..., output=..., mode=..., cval=..., origin=..., *, axes=...):
    """Calculate a multidimensional maximum filter.

    Parameters
    ----------
    %(input)s
    %(size_foot)s
    %(output)s
    %(mode_multiple)s
    %(cval)s
    %(origin_multiple)s
    axes : tuple of int or None, optional
        If None, `input` is filtered along all axes. Otherwise,
        `input` is filtered along the specified axes. When `axes` is
        specified, any tuples used for `size`, `origin`, and/or `mode`
        must match the length of `axes`. The ith entry in any of these tuples
        corresponds to the ith entry in `axes`.

    Returns
    -------
    maximum_filter : ndarray
        Filtered array. Has the same shape as `input`.

    Notes
    -----
    A sequence of modes (one per axis) is only supported when the footprint is
    separable. Otherwise, a single mode string must be provided.

    Examples
    --------
    >>> from scipy import ndimage, datasets
    >>> import matplotlib.pyplot as plt
    >>> fig = plt.figure()
    >>> plt.gray()  # show the filtered result in grayscale
    >>> ax1 = fig.add_subplot(121)  # left side
    >>> ax2 = fig.add_subplot(122)  # right side
    >>> ascent = datasets.ascent()
    >>> result = ndimage.maximum_filter(ascent, size=20)
    >>> ax1.imshow(ascent)
    >>> ax2.imshow(result)
    >>> plt.show()
    """
    ...

@_ni_docstrings.docfiller
def rank_filter(input, rank, size=..., footprint=..., output=..., mode=..., cval=..., origin=..., *, axes=...):
    """Calculate a multidimensional rank filter.

    Parameters
    ----------
    %(input)s
    rank : int
        The rank parameter may be less than zero, i.e., rank = -1
        indicates the largest element.
    %(size_foot)s
    %(output)s
    %(mode_reflect)s
    %(cval)s
    %(origin_multiple)s
    axes : tuple of int or None, optional
        If None, `input` is filtered along all axes. Otherwise,
        `input` is filtered along the specified axes.

    Returns
    -------
    rank_filter : ndarray
        Filtered array. Has the same shape as `input`.

    Examples
    --------
    >>> from scipy import ndimage, datasets
    >>> import matplotlib.pyplot as plt
    >>> fig = plt.figure()
    >>> plt.gray()  # show the filtered result in grayscale
    >>> ax1 = fig.add_subplot(121)  # left side
    >>> ax2 = fig.add_subplot(122)  # right side
    >>> ascent = datasets.ascent()
    >>> result = ndimage.rank_filter(ascent, rank=42, size=20)
    >>> ax1.imshow(ascent)
    >>> ax2.imshow(result)
    >>> plt.show()
    """
    ...

@_ni_docstrings.docfiller
def median_filter(input, size=..., footprint=..., output=..., mode=..., cval=..., origin=..., *, axes=...):
    """
    Calculate a multidimensional median filter.

    Parameters
    ----------
    %(input)s
    %(size_foot)s
    %(output)s
    %(mode_reflect)s
    %(cval)s
    %(origin_multiple)s
    axes : tuple of int or None, optional
        If None, `input` is filtered along all axes. Otherwise,
        `input` is filtered along the specified axes.

    Returns
    -------
    median_filter : ndarray
        Filtered array. Has the same shape as `input`.

    See Also
    --------
    scipy.signal.medfilt2d

    Notes
    -----
    For 2-dimensional images with ``uint8``, ``float32`` or ``float64`` dtypes
    the specialised function `scipy.signal.medfilt2d` may be faster. It is
    however limited to constant mode with ``cval=0``.

    Examples
    --------
    >>> from scipy import ndimage, datasets
    >>> import matplotlib.pyplot as plt
    >>> fig = plt.figure()
    >>> plt.gray()  # show the filtered result in grayscale
    >>> ax1 = fig.add_subplot(121)  # left side
    >>> ax2 = fig.add_subplot(122)  # right side
    >>> ascent = datasets.ascent()
    >>> result = ndimage.median_filter(ascent, size=20)
    >>> ax1.imshow(ascent)
    >>> ax2.imshow(result)
    >>> plt.show()
    """
    ...

@_ni_docstrings.docfiller
def percentile_filter(input, percentile, size=..., footprint=..., output=..., mode=..., cval=..., origin=..., *, axes=...):
    """Calculate a multidimensional percentile filter.

    Parameters
    ----------
    %(input)s
    percentile : scalar
        The percentile parameter may be less than zero, i.e.,
        percentile = -20 equals percentile = 80
    %(size_foot)s
    %(output)s
    %(mode_reflect)s
    %(cval)s
    %(origin_multiple)s
    axes : tuple of int or None, optional
        If None, `input` is filtered along all axes. Otherwise,
        `input` is filtered along the specified axes.

    Returns
    -------
    percentile_filter : ndarray
        Filtered array. Has the same shape as `input`.

    Examples
    --------
    >>> from scipy import ndimage, datasets
    >>> import matplotlib.pyplot as plt
    >>> fig = plt.figure()
    >>> plt.gray()  # show the filtered result in grayscale
    >>> ax1 = fig.add_subplot(121)  # left side
    >>> ax2 = fig.add_subplot(122)  # right side
    >>> ascent = datasets.ascent()
    >>> result = ndimage.percentile_filter(ascent, percentile=20, size=20)
    >>> ax1.imshow(ascent)
    >>> ax2.imshow(result)
    >>> plt.show()
    """
    ...

@_ni_docstrings.docfiller
def generic_filter1d(input, function, filter_size, axis=..., output=..., mode=..., cval=..., origin=..., extra_arguments=..., extra_keywords=...): # -> NDArray[float64] | NDArray[Any]:
    """Calculate a 1-D filter along the given axis.

    `generic_filter1d` iterates over the lines of the array, calling the
    given function at each line. The arguments of the line are the
    input line, and the output line. The input and output lines are 1-D
    double arrays. The input line is extended appropriately according
    to the filter size and origin. The output line must be modified
    in-place with the result.

    Parameters
    ----------
    %(input)s
    function : {callable, scipy.LowLevelCallable}
        Function to apply along given axis.
    filter_size : scalar
        Length of the filter.
    %(axis)s
    %(output)s
    %(mode_reflect)s
    %(cval)s
    %(origin)s
    %(extra_arguments)s
    %(extra_keywords)s

    Returns
    -------
    generic_filter1d : ndarray
        Filtered array. Has the same shape as `input`.

    Notes
    -----
    This function also accepts low-level callback functions with one of
    the following signatures and wrapped in `scipy.LowLevelCallable`:

    .. code:: c

       int function(double *input_line, npy_intp input_length,
                    double *output_line, npy_intp output_length,
                    void *user_data)
       int function(double *input_line, intptr_t input_length,
                    double *output_line, intptr_t output_length,
                    void *user_data)

    The calling function iterates over the lines of the input and output
    arrays, calling the callback function at each line. The current line
    is extended according to the border conditions set by the calling
    function, and the result is copied into the array that is passed
    through ``input_line``. The length of the input line (after extension)
    is passed through ``input_length``. The callback function should apply
    the filter and store the result in the array passed through
    ``output_line``. The length of the output line is passed through
    ``output_length``. ``user_data`` is the data pointer provided
    to `scipy.LowLevelCallable` as-is.

    The callback function must return an integer error status that is zero
    if something went wrong and one otherwise. If an error occurs, you should
    normally set the python error status with an informative message
    before returning, otherwise a default error message is set by the
    calling function.

    In addition, some other low-level function pointer specifications
    are accepted, but these are for backward compatibility only and should
    not be used in new code.

    """
    ...

@_ni_docstrings.docfiller
def generic_filter(input, function, size=..., footprint=..., output=..., mode=..., cval=..., origin=..., extra_arguments=..., extra_keywords=...): # -> NDArray[float64] | NDArray[Any]:
    """Calculate a multidimensional filter using the given function.

    At each element the provided function is called. The input values
    within the filter footprint at that element are passed to the function
    as a 1-D array of double values.

    Parameters
    ----------
    %(input)s
    function : {callable, scipy.LowLevelCallable}
        Function to apply at each element.
    %(size_foot)s
    %(output)s
    %(mode_reflect)s
    %(cval)s
    %(origin_multiple)s
    %(extra_arguments)s
    %(extra_keywords)s

    Returns
    -------
    generic_filter : ndarray
        Filtered array. Has the same shape as `input`.

    Notes
    -----
    This function also accepts low-level callback functions with one of
    the following signatures and wrapped in `scipy.LowLevelCallable`:

    .. code:: c

       int callback(double *buffer, npy_intp filter_size,
                    double *return_value, void *user_data)
       int callback(double *buffer, intptr_t filter_size,
                    double *return_value, void *user_data)

    The calling function iterates over the elements of the input and
    output arrays, calling the callback function at each element. The
    elements within the footprint of the filter at the current element are
    passed through the ``buffer`` parameter, and the number of elements
    within the footprint through ``filter_size``. The calculated value is
    returned in ``return_value``. ``user_data`` is the data pointer provided
    to `scipy.LowLevelCallable` as-is.

    The callback function must return an integer error status that is zero
    if something went wrong and one otherwise. If an error occurs, you should
    normally set the python error status with an informative message
    before returning, otherwise a default error message is set by the
    calling function.

    In addition, some other low-level function pointer specifications
    are accepted, but these are for backward compatibility only and should
    not be used in new code.

    Examples
    --------
    Import the necessary modules and load the example image used for
    filtering.

    >>> import numpy as np
    >>> from scipy import datasets
    >>> from scipy.ndimage import zoom, generic_filter
    >>> import matplotlib.pyplot as plt
    >>> ascent = zoom(datasets.ascent(), 0.5)

    Compute a maximum filter with kernel size 5 by passing a simple NumPy
    aggregation function as argument to `function`.

    >>> maximum_filter_result = generic_filter(ascent, np.amax, [5, 5])

    While a maximmum filter could also directly be obtained using
    `maximum_filter`, `generic_filter` allows generic Python function or
    `scipy.LowLevelCallable` to be used as a filter. Here, we compute the
    range between maximum and minimum value as an example for a kernel size
    of 5.

    >>> def custom_filter(image):
    ...     return np.amax(image) - np.amin(image)
    >>> custom_filter_result = generic_filter(ascent, custom_filter, [5, 5])

    Plot the original and filtered images.

    >>> fig, axes = plt.subplots(3, 1, figsize=(3, 9))
    >>> plt.gray()  # show the filtered result in grayscale
    >>> top, middle, bottom = axes
    >>> for ax in axes:
    ...     ax.set_axis_off()  # remove coordinate system
    >>> top.imshow(ascent)
    >>> top.set_title("Original image")
    >>> middle.imshow(maximum_filter_result)
    >>> middle.set_title("Maximum filter, Kernel: 5x5")
    >>> bottom.imshow(custom_filter_result)
    >>> bottom.set_title("Custom filter, Kernel: 5x5")
    >>> fig.tight_layout()

    """
    ...
