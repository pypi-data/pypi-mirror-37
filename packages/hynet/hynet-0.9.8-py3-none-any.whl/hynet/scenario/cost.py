"""
Representation of (injector) cost functions in *hynet*.
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

from hynet.types_ import hynet_float_


class PWLFunction:
    """
    Representation of a piecewise linear function ``f: R -> R``.

    Parameters
    ----------
    samples : (numpy.ndarray[.hynet_float_], numpy.ndarray[.hynet_float_]), optional
        Tuple ``(x, y)`` of ``x``- and ``y``-coordinates of sample points of
        the piecewise linear function, i.e., ``(x[0], y[0]), ..., (x[N], y[N])``.
    """

    def __init__(self, samples=None):
        """Create the PWL function with sample points 'samples'"""
        self._x = np.array([0, 1], dtype=hynet_float_)
        self._y = np.array([0, 0], dtype=hynet_float_)
        self.samples = ((0, 1), (0, 0)) if samples is None else samples

    @property
    def samples(self):
        """
        Return the tuple ``(x, y)`` of ``x``- and ``y``-coordinate arrays.
        """
        return self._x, self._y

    @samples.setter
    def samples(self, value):
        """
        Set the tuple ``(x, y)`` of ``x``- and ``y``-coordinate arrays.
        """
        if len(value) != 2:
            raise ValueError("Expecting a tuple (x, y) of coordinates.")
        x = np.array(value[0], dtype=hynet_float_)
        y = np.array(value[1], dtype=hynet_float_)
        if len(x) < 2 or len(x) != len(y) or x.ndim != 1 or y.ndim != 1:
            raise ValueError("Expecting a tuple (x, y) of coordinates "
                             "comprising at least two points.")
        if any(np.diff(x) <= 0):
            raise ValueError("The x-coordinate of samples must be "
                             "strictly increasing.")
        (self._x, self._y) = (x, y)

    def __repr__(self):
        if len(self._x) == 2:
            return str(np.asscalar(np.diff(self._y) / np.diff(self._x)))
        return '-'.join(['({0:g},{1:g})'.format(x, y)
                         for x, y in zip(self._x, self._y)])

    def __eq__(self, other):
        """Return True if the cost functions feature the same sample points."""
        if other is None:
            return False
        return (np.array_equal(self._x, other.samples[0]) and
                np.array_equal(self._y, other.samples[1]))

    def evaluate(self, x):
        """
        Evaluate the function at ``x``, i.e., return ``y = f(x)``.
        """
        result = interp1d(self._x, self._y,
                          kind='linear', fill_value='extrapolate')(x)
        if np.isscalar(x):
            return np.asscalar(result)
        return result

    def show(self):
        """
        Show the piecewise linear function.
        """
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(self._x, self._y,
                color='xkcd:sea blue', linestyle='-', linewidth=1)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        fig.tight_layout()
        fig.show()
        return fig

    def scale(self, scaling):
        """
        Scale the function by ``scaling``, i.e., ``f(x) -> scaling * f(x)``.
        """
        if scaling < 0:
            raise ValueError("Expecting a nonnegative scaling factor.")
        self._y *= scaling
        return self

    def is_convex(self):
        """
        Return ``True`` if the function is convex.
        """
        if len(self._x) == 2:
            # Affine function
            return True
        # Convex if curvature is nonnegative
        return all(np.diff(np.diff(self._y) / np.diff(self._x)) >= 0)

    def get_epigraph_polyhedron(self):
        """
        Return ``(A, b)`` such that ``f(x) = min{z in R: z*1 >= A*x + b}``.

        Note that ``f`` must be **convex**.
        """
        A = np.diff(self._y) / np.diff(self._x)        # Slope
        b = self._y[1:] - np.multiply(A, self._x[1:])  # Offset
        return A, b
