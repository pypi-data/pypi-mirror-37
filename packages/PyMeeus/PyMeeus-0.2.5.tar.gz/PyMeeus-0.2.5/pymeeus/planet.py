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


from Epoch import Epoch
from Coordinates import geometric_vsop_pos, apparent_vsop_pos


"""
.. module:: XXX
   :synopsis: Class to model XXX planet
   :license: GNU Lesser General Public License v3 (LGPLv3)

.. moduleauthor:: Dagoberto Salazar
"""


VSOP87_L = [
    # L0
    [
        [620347711.583, 0.00000000000, 0.00000000000],


    ],
    # L1
    [
        [334085627474.342, 0.00000000000, 0.00000000000],


    ],
    # L2
    [
        [58015.791, 2.04979463279, 3340.61242669980],


    ],
    # L3
    [
        [1482.423, 0.44434694876, 3340.61242669980],


    ],
    # L4
    [
        [113.969, 3.14159265359, 0.00000000000],


    ],
    # L5
    [
        [0.710, 4.04089996521, 6681.22485339960],


    ],
]
"""This table contains XXX' periodic terms (all of them) from the planetary
theory VSOP87 for the heliocentric longitude at the equinox of date (taken from
the 'D' solution). In Meeus' book a shortened version can be found in pages
421-424."""


VSOP87_B = [
    # B0
    [
        [3197134.986, 3.76832042432, 3340.61242669980],


    ],
    # B1
    [
        [350068.845, 5.36847836211, 3340.61242669980],


    ],
    # B2
    [
        [16726.690, 0.60221392419, 3340.61242669980],


    ],
    # B3
    [
        [606.506, 1.98050633529, 3340.61242669980],


    ],
    # B4
    [
        [11.334, 3.45724352586, 3340.61242669980],


    ],
    # B5
    [
        [0.457, 4.86794125358, 3340.61242669980],


    ],
]
"""This table contains XXX' periodic terms (all of them) from the planetary
theory VSOP87 for the heliocentric latitude at the equinox of date (taken from
the 'D' solution). In Meeus' book a shortened version can be found in pages
424-425."""


VSOP87_R = [
    # R0
    [
        [153033488.276, 0.00000000000, 0.00000000000],


    ],
    # R1
    [
        [1107433.340, 2.03250524950, 3340.61242669980],


    ],
    # R2
    [
        [44242.247, 0.47930603943, 3340.61242669980],


    ],
    # R3
    [
        [1113.107, 5.14987350142, 3340.61242669980],


    ],
    # R4
    [
        [19.552, 3.58211650473, 3340.61242669980],


    ],
    # R5
    [
        [0.476, 2.47617204701, 6681.22485339960],


    ],
]
"""This table contains XXX' periodic terms (all of them) from the planetary
theory VSOP87 for the radius vector at the equinox of date (taken from the 'D'
solution). In Meeus' book a shortened version can be found in pages 425-426."""


class XXX(object):
    """
    Class XXX models that planet.
    """

    @staticmethod
    def geometric_heliocentric_position(epoch, toFK5=True):
        """"This method computes the geometric heliocentric position of planet
        XXX for a given epoch, using the VSOP87 theory.

        :param epoch: Epoch to compute XXX position, as an Epoch object
        :type epoch: :py:class:`Epoch`
        :param toFK5: Whether or not the small correction to convert to the FK5
            system will be applied or not
        :type toFK5: bool

        :returns: A tuple with the heliocentric longitude and latitude (as
            :py:class:`Angle` objects), and the radius vector (as a float,
            in astronomical units), in that order
        :rtype: tuple
        :raises: TypeError if input values are of wrong type.

        >>> epoch = Epoch(2018, 10, 27.0)
        >>> l, b, r = XXX.geometric_heliocentric_position(epoch)
        >>> print(round(l.to_positive(), 4))
        2.0015
        >>> print(round(b, 4))
        -1.3683
        >>> print(round(r, 5))
        1.39306
        """

        # First check that input values are of correct types
        if not isinstance(epoch, Epoch):
            raise TypeError("Invalid input types")
        # Second, call auxiliary function in charge of computations
        return geometric_vsop_pos(epoch, VSOP87_L, VSOP87_B, VSOP87_R, toFK5)

    @staticmethod
    def apparent_heliocentric_position(epoch):
        """"This method computes the apparent heliocentric position of planet
        XXX for a given epoch, using the VSOP87 theory.

        :param epoch: Epoch to compute XXX position, as an Epoch object
        :type epoch: :py:class:`Epoch`

        :returns: A tuple with the heliocentric longitude and latitude (as
            :py:class:`Angle` objects), and the radius vector (as a float,
            in astronomical units), in that order
        :rtype: tuple
        :raises: TypeError if input values are of wrong type.
        """

        # First check that input values are of correct types
        if not isinstance(epoch, Epoch):
            raise TypeError("Invalid input types")
        # Second, call auxiliary function in charge of computations
        return apparent_vsop_pos(epoch, VSOP87_L, VSOP87_B, VSOP87_R)


def main():

    # Let's define a small helper function
    def print_me(msg, val):
        print("{}: {}".format(msg, val))

    # Let's show some uses of Venus class
    print("\n" + 35 * "*")
    print("*** Use of XXX class")
    print(35 * "*" + "\n")

    # Let's now compute the heliocentric position for a given epoch
    epoch = Epoch(2018, 10, 27.0)
    lon, lat, r = XXX.geometric_heliocentric_position(epoch)
    print_me("Geometric Heliocentric Longitude", lon.to_positive())
    print_me("Geometric Heliocentric Latitude", lat)
    print_me("Radius vector", r)


if __name__ == "__main__":

    main()
