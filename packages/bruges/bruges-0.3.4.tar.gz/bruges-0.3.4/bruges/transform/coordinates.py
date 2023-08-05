# -*- coding: utf-8 -*-
"""
Coordinate transformation. A class for converting between
seismic survey inline-xline coordinates and real-world UTM
coordinates.

:copyright: 2018 Agile Geoscience
:license: Apache 2.0
"""
import numpy as np
from ..util.transformations import affine_matrix_from_points


class CoordTransform(object):
    def __init__(self, ix, xy):
        ix = np.array(ix)
        xy = np.array(xy)
        if ix.shape[1] == 2:
            ix = ix[:3].T
        if xy.shape[1] == 2:
            xy = xy[:3].T
        self.A = affine_matrix_from_points(ix, xy)

    def __call__(self, p):
        p = np.asanyarray(p)
        return np.dot(self.A, np.append(p, [1]))[:2]

    def forward(self, p):
        p = np.asanyarray(p)
        return self(p)

    def reverse(self, q):
        p = np.dot(np.linalg.pinv(self.A), np.append(q, [1]))[:2]
        return np.rint(p).astype(np.int)
