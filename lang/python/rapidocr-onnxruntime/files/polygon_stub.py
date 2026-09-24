"""Minimal stand-in for shapely.geometry.Polygon, providing only the two
properties the text detector uses (area and perimeter of a simple polygon).

shapely is a hard dependency of rapidocr_onnxruntime, but it needs the GEOS
library, which is not available on every target (e.g. OpenWrt). The values are
computed with the shoelace formula, so the result is the same as shapely's for
the quadrilaterals produced by the DB postprocessing.
"""

import numpy as np


class Polygon:
    def __init__(self, points):
        pts = np.asarray(points, dtype=np.float64).reshape(-1, 2)
        x = pts[:, 0]
        y = pts[:, 1]
        x_next = np.roll(x, -1)
        y_next = np.roll(y, -1)
        self.area = float(abs(np.dot(x, y_next) - np.dot(x_next, y)) / 2.0)
        self.length = float(np.sum(np.hypot(x_next - x, y_next - y)))
