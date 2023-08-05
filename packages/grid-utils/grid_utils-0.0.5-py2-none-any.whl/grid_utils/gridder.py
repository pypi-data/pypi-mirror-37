# -*- coding:utf-8 -*-

import six
import numpy as np
from pyproj import Proj

from .exceptions import *


class NullProj(object):
    """
    Similar to pyproj.Proj, but NullProj does not do actual conversion.
    """
    @property
    def srs(self):
        return ''

    def __call__(self, x, y, **kwargs):
        return x, y


class GridderBase(object):
    """Gridder is a helper for i, j <-> x, y conversion, etc."""
    def i2x(self, *args):
        """Convert i, j, ... -> x, y, ..."""
        raise NotImplementedError

    def x2i(self, *args, **kwargs):
        """Convert x, y, ... -> i, j, ..."""
        raise NotImplementedError

    def copy(self, **kwargs):
        kws = self.dump()
        kws.update(kwargs)
        new_gridder = self.__class__(**kws)
        return new_gridder

    def calibrate(self, x0, y0, x1=None, y1=None):
        return

    def dump(self):
        return {}


class XYGridderBase(GridderBase):
    """
    Requires self.X & self.Y.
    """
    def get_bounding_ij(self, x1, x2, y1, y2):
        bad = ~((self.X >= x1) & (self.X <= x2) & (self.Y >= y1) & (self.Y <= y2))
        x_bad = np.alltrue(bad, axis=0)
        y_bad = np.alltrue(bad, axis=1)
        x_points = np.argwhere(np.diff(np.r_[True, x_bad, True])).reshape(-1, 2)
        y_points = np.argwhere(np.diff(np.r_[True, y_bad, True])).reshape(-1, 2)
        i1, i2 = (-1, -1) if x_points.shape[0] == 0 else x_points[0]
        j1, j2 = (-1, -1) if y_points.shape[0] == 0 else y_points[0]
        return i1, i2, j1, j2

    def check_bound(self, i, j, int_index=True):
        start = -0.5
        subtracted = 1
        if int_index:
            start = 0
            if int_index in ('lowerleft', 'll'):
                subtracted = 2
        if np.isscalar(i):
            if (i >= start and i <= self.nx-subtracted) and (j >= start and j <= self.ny-subtracted):
                return i, j
            else:
                raise OutOfGridBound("i: {}, j: {} is out of bound!".format(i, j))
        else:
            i = np.where((i >= start) & (i <= self.nx - subtracted), i, np.nan)
            j = np.where((j >= start) & (j <= self.ny - subtracted), j, np.nan)
            return i, j


class XYProjGridder(XYGridderBase):
    def __init__(self, proj_info, nx, ny, dx, dy, x_orig=0.0, y_orig=0.0):
        self.proj_info = proj_info
        if not proj_info:
            self.proj = NullProj()
        elif isinstance(proj_info, dict):
            self.proj = Proj(**proj_info)
        else:  # Treat as proj_string
            self.proj = Proj(str(proj_info))  # TODO: check PY3 compatibility.

        self.nx = nx
        self.ny = ny
        self.dx = dx
        self.dy = dy
        self.x_orig = x_orig
        self.y_orig = y_orig

        self.X, self.Y = self._createXY()

    def i2x(self, i, j):
        px = i * self.dx + self.x_orig
        py = j * self.dy + self.y_orig
        return self.proj(px, py, inverse=True)

    def x2i(self, x, y, int_index=True, check_bound=None):
        px, py = self.proj(x, y)
        i = (px - self.x_orig) / self.dx
        j = (py - self.y_orig) / self.dy
        if int_index:
            if int_index in ('lowerleft', 'll'):
                i = np.floor(i)
                j = np.floor(j)
            else:
                i = np.round(i)
                j = np.round(j)
            if np.isscalar(i):
                i = int(i)
                j = int(j)
            else:
                i = i.astype('i')
                j = j.astype('i')

        if check_bound:
            return self.check_bound(i, j, int_index=int_index)
        else:
            return i, j

    def calibrate(self, x0, y0, x1=None, y1=None):
        px0, py0 = self.proj(x0, y0)

        self.x_orig = px0
        self.y_orig = py0

        if x1 is not None and y1 is not None:
            px1, py1 = self.proj(x1, y1)
            self.dx = px1 - px0
            self.dy = py1 - py0

        self.X, self.Y = self._createXY()

    def _createXY(self):
        jj, ii = np.mgrid[0:self.ny, 0:self.nx]
        xx, yy = self.i2x(ii, jj)
        return xx, yy

    def dump(self):
        return {
            "proj_info": self.proj.srs,
            "nx": self.nx, "ny": self.ny, "dx": self.dx, "dy": self.dy,
            "x_orig": self.x_orig, "y_orig": self.y_orig
        }


class XYIrregularGridder(XYGridderBase):
    # TODO: use kdtree.
    def __init__(self, X, Y):
        X = np.array(X)
        Y = np.array(Y)
        if X.ndim == 1:
            self.X, self.Y = np.meshgrid(X, Y)
        else:
            self.X, self.Y = X, Y

        self.ny, self.nx = X.shape

    def i2x(self, i, j, *args, **kwargs):
        return self.X[j, i], self.Y[j, i]

    def x2i(self, x, y, *args, **kwargs):
        distances = np.hypot(self.X-x, self.Y-y)
        flat_i = np.argmin(distances)
        nx = self.X.shape[1]
        return flat_i / self.nx, flat_i % self.nx

    def dump(self):
        return {
            "X": self.X,
            "Y": self.Y,
            "nx": self.nx,
            "ny": self.ny,
        }
