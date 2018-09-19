# (C) British Crown Copyright 2018, Met Office
#
# This file is part of Iris.
#
# Iris is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Iris is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Iris.  If not, see <http://www.gnu.org/licenses/>.
"""Common test code for `iris.plot.pcolor` and `iris.plot.pcolormesh`."""

from __future__ import (absolute_import, division, print_function)
from six.moves import (filter, input, map, range, zip)  # noqa

# Import iris.tests first so that some things can be initialised before
# importing anything else.
import iris.tests as tests

import numpy as np

from iris.tests.stock import simple_2d
from iris.tests.unit.plot import MixinCoords

if tests.MPL_AVAILABLE:
    import iris.plot as iplt


class MixinStringCoordPlot(object):
    # Mixin for common string-coord tests on pcolor/pcolormesh.
    # To use, make a class that inherits from this *and*
    # :class:`iris.tests.unit.plot.TestGraphicStringCoord`,
    # and defines "self.blockplot_func()", to return the `iris.plot` function.
    def test_yaxis_labels(self):
        self.blockplot_func()(self.cube, coords=('bar', 'str_coord'))
        self.assertBoundsTickLabels('yaxis')

    def test_xaxis_labels(self):
        self.blockplot_func()(self.cube, coords=('str_coord', 'bar'))
        self.assertBoundsTickLabels('xaxis')

    def test_xaxis_labels_with_axes(self):
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_xlim(0, 3)
        self.blockplot_func()(self.cube, coords=('str_coord', 'bar'), axes=ax)
        plt.close(fig)
        self.assertPointsTickLabels('xaxis', ax)

    def test_yaxis_labels_with_axes(self):
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_ylim(0, 3)
        self.blockplot_func()(self.cube, axes=ax, coords=('bar', 'str_coord'))
        plt.close(fig)
        self.assertPointsTickLabels('yaxis', ax)

    def test_geoaxes_exception(self):
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_subplot(111)
        self.assertRaises(TypeError, self.blockplot_func(),
                          self.lat_lon_cube, axes=ax)
        plt.close(fig)


class Mixin2dCoordsPlot(MixinCoords):
    # Mixin for common coordinate tests on pcolor/pcolormesh.
    # To use, make a class that inherits from this *and*
    # :class:`iris.tests.IrisTest`,
    # and defines "self.blockplot_func()", to return the `iris.plot` function.
    def blockplot_setup(self):
        # We have a 2d cube with dimensionality (bar: 3; foo: 4)
        self.cube = simple_2d(with_bounds=True)
        coord = self.cube.coord('foo')
        self.foo = coord.contiguous_bounds()
        self.foo_index = np.arange(coord.points.size + 1)
        coord = self.cube.coord('bar')
        self.bar = coord.contiguous_bounds()
        self.bar_index = np.arange(coord.points.size + 1)
        self.data = self.cube.data
        self.dataT = self.data.T
        self.draw_func = self.blockplot_func()
        patch_target_name = 'matplotlib.pyplot.' + self.draw_func.__name__
        self.mpl_patch = self.patch(patch_target_name)


if __name__ == "__main__":
    tests.main()
