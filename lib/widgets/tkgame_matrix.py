#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    tkGAME - all-in-one Game library for Tkinter

    Copyright (c) 2014+ Raphaël Seban <motus@laposte.net>

    This program is free software: you can redistribute it and/or
    modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation, either version 3 of
    the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.

    If not, see http://www.gnu.org/licenses/
"""


class TkGameMatrix:
    """
        Game Matrix for Tkinter GUI environment
    """

    # class constants
    TOP_LEFT = "top left"
    TOP_RIGHT = "top right"
    BOTTOM_LEFT = "bottom left"
    BOTTOM_RIGHT = "bottom right"


    def __init__ (self, matrix_data, matrix_defs, cellsize=0):
        """
            class constructor
        """
        self.data = matrix_data
        self.defs = matrix_defs
        self.cellsize = cellsize
    # end def


    def bbox (self):
        """
            returns estimated graphical bounding box of the matrix
        """
        return (0, 0, self.columns * self.cellsize, self.rows * self.cellsize)
    # end def


    def center_xy (self, row, column):
        """
            returns center (x, y) coordinates of a matrix cell
            located at (row, column);
        """
        return (
            (column + 0.5) * self.cellsize, (row + 0.5) * self.cellsize
        )
    # end def


    def corner_xy (self, row, column, corner=None):
        """
            returns top/bottom left/right (x, y) corner coordinates
            of a matrix cell located at (row, column); parameter
            @corner should be one of self.TOP_LEFT, self.TOP_RIGHT,
            self.BOTTOM_LEFT or self.BOTTOM_RIGHT; will default to
            self.TOP_LEFT if omitted or incorrect param value;
        """
        dx, dy = {
            self.TOP_LEFT: (0, 0),
            self.TOP_RIGHT: (1, 0),
            self.BOTTOM_LEFT: (0, 1),
            self.BOTTOM_RIGHT: (1, 1),
        }.get(corner) or (0, 0)
        return (
            (column + dx) * self.cellsize, (row + dy) * self.cellsize
        )
    # end def


    def row_column (self, x, y):
        """
            converts an (x, y) position to (row, column) position
        """
        return (x//self.cellsize, y//self.cellsize)
    # end def


    def width_height (self):
        """
            returns estimated graphical (width, height) of the matrix
        """
        return (self.columns * self.cellsize, self.rows * self.cellsize)
    # end def


    @property
    def cellsize (self):
        """
            size of a square matrix cell
        """
        return self.__cellsize
    # end def

    @cellsize.setter
    def cellsize (self, value):
        self.__cellsize = abs(int(value))
    # end def

    @cellsize.deleter
    def cellsize (self):
        del self.__cellsize
    # end def


    @property
    def data (self):
        """
            matrix data
        """
        return self.__data
    # end def

    @data.setter
    def data (self, value):
        if isinstance(value, list):
            self.__data = value
            self.rows = len(value)
            self.columns = max(0, 0, *map(len, value))
        else:
            raise TypeError(
                "matrix data must be of type 'list'."
            )
        # end if
    # end def

    @data.deleter
    def data (self):
        del self.__data
    # end def

# end class TkGameMatrix
