# -*- coding: utf-8 -*-


# PyMeeus: Python module implementing astronomical algorithms.
# Copyright (C) 2018  Dagoberto Salazar
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from pymeeus.base import TOL
from pymeeus.Saturn import Saturn
from pymeeus.Epoch import Epoch


# Saturn class

def test_saturn_geometric_heliocentric_position():
    """Tests the geometric_heliocentric_position() method of Saturn class"""

    epoch = Epoch(2018, 10, 27.0)
    lon, lat, r = Saturn.geometric_heliocentric_position(epoch)

    assert abs(round(lon.to_positive(), 4) - 279.5108) < TOL, \
        "ERROR: 1st geometric_heliocentric_position() test doesn't match"

    assert abs(round(lat, 4) - 0.6141) < TOL, \
        "ERROR: 2nd geometric_heliocentric_position() test doesn't match"

    assert abs(round(r, 5) - 10.06266) < TOL, \
        "ERROR: 3rd geometric_heliocentric_position() test doesn't match"
