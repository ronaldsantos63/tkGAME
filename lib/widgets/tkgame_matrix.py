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

    CELLSIZE = 64


    def __init__ (self, **kw):
        """
            class constructor
        """
        self.__internal_data = dict()
        self.rows = kw.get("rows") or 0
        self.columns = kw.get("columns") or 0
        self.cellsize = kw.get("cellsize") or self.CELLSIZE
        # external matrix data support
        self.resize(kw.get("data"))
    # end def


    def _rebind (self, xy, bbox, circular_xy=None):
        """
            protected method - generic rebinding implementation;
        """
        # inits
        x, y = xy
        xmin, ymin, xmax, ymax = bbox
        # circular rebindings
        if circular_xy:
            circular_x, circular_y = circular_xy
            if circular_x:
                if x < xmin:
                    x = max(xmin, xmax)
                elif x > xmax:
                    x = xmin
                # end if
            # end if
            if circular_y:
                if y < ymin:
                    y = max(ymin, ymax)
                elif y > ymax:
                    y = ymin
                # end if
            # end if
        # classical rebindings
        else:
            x = max(xmin, min(xmax, x))
            y = max(ymin, min(ymax, y))
        # end if
        # return results
        return (x, y)
    # end def


    def at (self, row_column):
        """
            retrieves object at row_column = (row, column), if exists;
        """
        return self.internal_data.get(row_column)
    # end def


    def at_xy (self, xy):
        """
            retrieves object at (x, y) converted to matrix location
            (row, column) or None if object is not found;
        """
        return self.at(self.row_column(xy))
    # end def


    def bbox (self):
        """
            returns matrix bounding box;
        """
        return (0, 0, max(0, self.rows - 1), max(0, self.columns - 1))
    # end def


    def bbox_xy (self):
        """
            returns estimated graphical bounding box of the matrix;
        """
        return (
            0, 0,
            max(0, self.columns * self.cellsize - 1),
            max(0, self.rows * self.cellsize - 1)
        )
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
        self.__cellsize = max(0, int(value))
    # end def

    @cellsize.deleter
    def cellsize (self):
        del self.__cellsize
    # end def


    def center_xy (self, row_column):
        """
            returns center (x, y) coordinates of a matrix cell
            located at (row, column);
        """
        row, column = row_column
        return (
            (column + 0.5) * self.cellsize, (row + 0.5) * self.cellsize
        )
    # end def


    def coords (self):
        """
            returns list of available (row, column) coordinate tuples;
        """
        return self.internal_data.keys()
    # end def


    def corner_xy (self, row_column, corner=None):
        """
            returns top/bottom left/right (x, y) corner coordinates
            of a matrix cell located at (row, column);
            parameter @corner should be one of self.TOP_LEFT,
            self.TOP_RIGHT, self.BOTTOM_LEFT or self.BOTTOM_RIGHT;
            will default to self.TOP_LEFT if omitted or incorrect
            param value;
        """
        # inits
        row, column = row_column
        # relative_row, relative_column
        rr, rc = {
            self.TOP_LEFT: (0, 0),
            self.TOP_RIGHT: (0, 1),
            self.BOTTOM_LEFT: (1, 0),
            self.BOTTOM_RIGHT: (1, 1),
        }.get(corner) or (0, 0)
        return ((column + rc) * self.cellsize, (row + rr) * self.cellsize)
    # end def


    @property
    def internal_data (self):
        """
            matrix internal data (READ-ONLY property);
        """
        return self.__internal_data
    # end def

    @internal_data.setter
    def internal_data (self, value):
        """
            forbidden - READ-ONLY internal data
        """
        raise TkGameMatrixError(
            "'internal_data' attribute is READ-ONLY."
        )
    # end def

    @internal_data.deleter
    def internal_data (self):
        del self.__internal_data
    # end def


    def drop (self, row_column, raise_error=False):
        """
            deletes object located at (row, column);
            if @raise_error is True and no object found, raises
            TkGameMatrixCellError;
        """
        # inits
        _object = self.at(row_column)
        # got something to delete?
        if _object:
            # silent drops...
            self.internal_data.pop(row_column, None)
        # error handling
        elif raise_error:
            # raise error
            raise TkGameMatrixCellError(
                "while trying to delete: "
                "no object found in matrix cell."
            )
        # end if
    # end def


    def drop_xy (self, xy, raise_error=False):
        """
            deletes object located at (x, y) adjusted to matrix
            (row, column) location;
            if @raise_error is True and no object found, raises
            TkGameMatrixCellError;
        """
        self.drop(self.row_column(xy), raise_error)
    # end def


    def duplicate (self, from_rowcol, to_rowcol, raise_error=False):
        """
            duplicates object located at from_rowcol into to_rowcol
            location;
            if @raise_error is True:
            - raises TkGameMatrixCellError if destination is not None,
            - raises TkGameMatrixCellError if source is None;
        """
        self.move(from_rowcol, to_rowcol, raise_error, duplicate=True)
    # end def


    def duplicate_xy (self, from_xy, to_xy, raise_error=False):
        """
            duplicates object located at from_xy into to_xy all
            adjusted to matrix (row, column) locations;
            if @raise_error is True:
            - raises TkGameMatrixCellError if destination is not None,
            - raises TkGameMatrixCellError if source is None;
        """
        self.move_xy(from_xy, to_xy, raise_error, duplicate=True)
    # end def


    def move (self, from_rowcol, to_rowcol,
                                    raise_error=False, duplicate=False):
        """
            absolute move from (row0, column0) to (row1, column1);
            if @raise_error is True:
            - raises TkGameMatrixCellError if destination is not None,
            - raises TkGameMatrixCellError if source is None;
        """
        # look for destination object
        _object = self.at(to_rowcol)
        # error handling
        if _object and raise_error:
            raise TkGameMatrixCellError(
                "while trying to move/duplicate: "
                "destination cell is busy."
            )
        # it's OK, let's try to move/duplicate
        else:
            # look for source object
            _object = self.at(from_rowcol)
            # got something?
            if _object:
                # move it!
                self.set_at(to_rowcol, _object)
                # no duplication (simple move)?
                if not duplicate:
                    # remove from source location
                    self.internal_data.pop(from_rowcol, None)
                # end if
            # no source object found
            elif raise_error:
                # error handling
                raise TkGameMatrixCellError(
                    "while trying to move/duplicate: "
                    "no object found in source cell."
                )
            # end if
        # end if
    # end def


    def move_xy (self, from_xy, to_xy,
                                    raise_error=False, duplicate=False):
        """
            absolute move from (x0, y0) to (x1, y1) all adjusted to
            matrix (row, column) locations;
            if @raise_error is True:
            - raises TkGameMatrixCellError if destination is not None,
            - raises TkGameMatrixCellError if source is None;
        """
        self.move(
            self.row_column(from_xy),
            self.row_column(to_xy),
            raise_error,
            duplicate
        )
    # end def


    def objects (self):
        """
            returns list of matrix' registered objects;
        """
        return self.internal_data.values()
    # end def


    def rebind (self, row_column, circular=False):
        """
            rebinds (row, column) matrix location to fit into
            current matrix bounding box (bbox);
            if @circular is True, any overflow will return to zero;
            returns new rebound (row, column) coordinates;
        """
        # return results
        return self._rebind(row_column, self.bbox(), circular)
    # end def


    def rebind_xy (self, xy, circular=False):
        """
            rebinds (x, y) coordinates to fit into current matrix
            bounding box (bbox_xy);
            if @circular is True, any overflow will return to zero;
            returns new rebound (x, y) coordinates;
        """
        # return results
        return self._rebind(xy, self.bbox_xy(), circular)
    # end def


    def rel_at (self, from_rowcol, rel_rowcol):
        """
            retrieves object at relative location, if exists;
        """
        # inits
        row, column = from_rowcol
        # relative_row, relative_column
        rr, rc = rel_rowcol
        # get object
        return self.at((row + rr, column + rc))
    # end def


    def rel_at_xy (self, from_xy, rel_xy):
        """
            retrieves object at a relative (x, y) location, if any;
        """
        # inits
        x, y = from_xy
        rel_x, rel_y = rel_xy
        return self.at(self.row_column((x + rel_x, y + rel_y)))
    # end def


    def rel_duplicate (self, from_rowcol, rel_rowcol, raise_error=False):
        """
            duplicates object located at from_rowcol to relative
            rel_rowcol location;
            if @raise_error is True:
            - raises TkGameMatrixCellError if destination is not None,
            - raises TkGameMatrixCellError if source is None;
        """
        self.rel_move(
            from_rowcol, rel_rowcol, raise_error, duplicate=True
        )
    # end def


    def rel_duplicate_xy (self, from_xy, rel_xy, raise_error=False):
        """
            duplicates object located at from_xy into relative
            location rel_xy all adjusted to matrix (row, column)
            locations;
            if @raise_error is True:
            - raises TkGameMatrixCellError if destination is not None,
            - raises TkGameMatrixCellError if source is None;
        """
        self.rel_move_xy(from_xy, rel_xy, raise_error, duplicate=True)
    # end def


    def rel_move (self, from_rowcol, rel_rowcol,
                                    raise_error=False, duplicate=False):
        """
            relative move from (row, column) to (row + rel_row,
            column + rel_column);
            if @raise_error is True:
            - raises TkGameMatrixCellError if destination is not None,
            - raises TkGameMatrixCellError if source is None;
        """
        # inits
        row, column = from_rowcol
        rr, rc = rel_rowcol
        self.move(
            from_rowcol,
            (row + rr, column + rc),
            raise_error,
            duplicate
        )
    # end def


    def rel_move_xy (self, from_xy, rel_xy,
                                    raise_error=False, duplicate=False):
        """
            relative move from (x, y) to (x + rel_x, y + rel_y)
            using rel_xy all adjusted to matrix (row, column)
            locations;
            if @raise_error is True:
            - raises TkGameMatrixCellError if destination is not None,
            - raises TkGameMatrixCellError if source is None;
        """
        # inits
        x, y = from_xy
        rx, ry = rel_xy
        self.move_xy(from_xy, (x + rx, y + ry), raise_error, duplicate)
    # end def


    def resize (self, matrix_data):
        """
            resizes inner matrix (rows, columns) along with
            @matrix_data;
            this parameter must be at least a list of iterables;
        """
        # param controls
        if matrix_data:
            # inits
            self.data = list(matrix_data)
            self.rows = len(self.data)
            self.columns = max(0, 0, *map(len, self.data))
            # reset internal data
            self.internal_data.clear()
            # return results
            return (self.rows, self.columns)
        # end if
        # no data, no dims
        return (0, 0)
    # end def


    def row_column (self, xy):
        """
            converts an xy = (x, y) position to (row, column) position
        """
        # inits
        x, y = xy
        return (y//self.cellsize, x//self.cellsize)
    # end def


    def set_at (self, row_column, object_):
        """
            sets object at row_column = (row, column);
        """
        self.internal_data[row_column] = object_
    # end def


    def set_at_xy (self, xy, object_):
        """
            sets object at xy = (x, y) converted to a common matrix
            (row, column) location;
        """
        self.internal_data[self.row_column(xy)] = object_
    # end def


    def width_height (self):
        """
            returns estimated graphical (width, height) of the matrix
        """
        return (self.columns * self.cellsize, self.rows * self.cellsize)
    # end def

# end class TkGameMatrix


# exception handling

class TkGameMatrixError (Exception):
    """
        handles matrix specific errors;
    """
    pass
# end class TkGameMatrixError


# exception handling

class TkGameMatrixCellError (Exception):
    """
        handles matrix' cell specific errors;
    """
    pass
# end class TkGameMatrixCellError
