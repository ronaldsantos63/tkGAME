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

# lib imports
import random


# module scope global var

__DEBUG__ = False
#~ __DEBUG__ = True


# module scope function defs

def euler_latin_square (base_sequence=None):
    """
        Leonhard Euler's historical 'Latin Square' generation
        algorithm; latin squares are known to fit only the two first
        rules of Sudoku: ITEMS must appear only ONCE in each ROW and in
        each COLUMN; but latin squares do generally *NOT* fit the third
        rule of Sudoku: ITEMS must appear only ONCE in each BOX region;
        latin squares are therefore quite good crash tests for Sudoku
        grid validation algorithms;
    """
    # ensure subscriptable
    _base = tuple(base_sequence or range(1, 10))
    # nb of items
    _bl = len(_base)
    # return latin square
    return [
        _base[(_i + _i // _bl) % _bl]
        for _i in range(_bl**2)
    ]
# end def


def is_correct_grid (grid_data, base_sequence=None):
    """
        returns True if @grid_data sequence list of items is fully
        compliant with all Sudoku policies (each ITEM appears only ONCE
        in a given UNIT), False otherwise; parameter @base_sequence
        allows to know which ITEMS to compare; will be set to classical
        Sudoku [1..9] sequence by default, if omitted;
    """
    # ensure subscriptable
    _matrix = tuple(grid_data)
    # get base sequence
    _base = set(base_sequence or range(1, 10))
    print("verifying harmony")
    # verify global harmony
    if set(_matrix) != _base: return False
    # verify more detailed
    _size = _bl = len(_base)
    _chutes = _box_size = _bs = _bl**0.5
    # do we have a correct Sudoku grid?
    if _bs != int(_bs):
        raise ValueError(
            "invalid Sudoku grid size: {0} x {0}".format(_bl)
        )
    # end if
    # reset value
    _bs = int(_bs)
    print("verifying rows")
    # browse rows
    for _row in range(_size):
        # not good?
        if set(_matrix[_row * _size:(_row + 1) * _size]) != _base:
            # failed
            return False
        # end if
    # end for
    print("verifying columns")
    # browse columns
    for _column in range(_size):
        # not good?
        if set(_matrix[_column::_size]) != _base:
            # failed
            return False
        # end if
    # end for
    print("verifying boxes")
    # get boxes
    _boxes = [
        [
            _matrix[(_r0 * _bs + _row) * _bl + _c0 * _bs + _column]
            for _row in range(_bs)
            for _column in range(_bs)
        ]
        for _r0 in range(_bs)
        for _c0 in range(_bs)
    ]
    # browse boxes
    for _box in _boxes:
        # not good?
        if set(_box) != _base:
            # failed
            return False
        # end if
    # end for
    print("all is OK.")
    # succeeded
    return True
# end def


def lers2_sudoku_grid (base_sequence=None):
    """
        Leonhard Euler and Raphaël Seban (LERS) algorithm (v2);
        optimized version of SudokuMatrix.algo_euler_latin_square()
        generation method (LERS1); this algorithm (LERS2) was fitted on
        Tuesday 10th, 2015, in about 3 hours (including tests); LERS2
        uses base sequence simple index reading (no sequence rotation)
        and a 1-pass loop to generate a fully playable Sudoku grid
        between 9! = 362,880 distinct possibilities; LERS2 algorithm is
        about 10 times faster than LERS1;
    """
    # ensure subscriptable
    _base = tuple(base_sequence or range(1, 10))
    # nb of items
    _bl = len(_base)
    # box size = sqrt(_bl)
    _bs = int(_bl**0.5)
    # Sudoku chute rectangle area (constant)
    _ca = _bl * _bs
    # answer values
    return [
        _base[(_i + _bs * (_i // _bl) + _i // _ca) % _bl]
        for _i in range(_bl**2)
    ]
# end def


def rotate_left (sequence, inplace=False):
    """
        rotates @sequence from right to left; if @inplace == True,
        rotates @sequence object itself (must be a mutable list or at
        least a subclass of it in this case); returns copy of rotated
        sequence otherwise (@sequence must be subscriptable e.g. str,
        list, tuple or a subclass);
    """
    # inplace asked?
    if inplace:
        # not empty?
        if sequence:
            # object must be a mutable sequence (list)
            sequence.append(sequence.pop(0))
        # end if
        # return sequence itself
        return sequence
    # copy instance
    else:
        # object must be subscriptable
        return sequence[1:] + sequence[0:1]
    # end if
# end def


def rotate_right (sequence, inplace=False):
    """
        rotates @sequence from left to right; if @inplace == True,
        rotates @sequence object itself (must be a mutable list or
        at least a subclass of it in this case); returns copy of
        rotated sequence otherwise (@sequence must be subscriptable
        e.g. str, list, tuple or a subclass);
    """
    # inplace asked?
    if inplace:
        # not empty?
        if sequence:
            # object must be a mutable sequence (list)
            sequence.insert(0, sequence.pop(-1))
        # end if
        # return sequence itself
        return sequence
    # copy instance
    else:
        # object must be subscriptable
        return sequence[-1:] + sequence[:-1]
    # end if
# end def



class Matrix (list):
    """
        Generic matrix-like sequence manager;
        This matrix is a subclass of Python's list class;
        This matrix can be used as a Python list sequence (with some
        additional features);
    """

    def __init__ (self, **kw):
        """
            class constructor;
        """
        # super class inits
        super().__init__()
        # reset matrix
        self.reset(**kw)
    # end def


    def __repr__ (self):
        """
            for debugging session;
        """
        # debug mode?
        if __DEBUG__ and __debug__:
            # return string representation
            return "\n{classname} (\n{data}\n)".format(
                classname=self.__class__.__name__,
                data="\n".join(map(repr, self.get_rows()))
            )
        # NO debug mode
        else:
            # super class representation
            return super().__repr__()
        # end if
    # end def


    def at (self, row, column):
        """
            retrieves matrix' cell located at (@row, @column); will
            raise IndexError if location is out of matrix' bounds;
        """
        # ensure location is in matrix' bounds
        self.ensure_inbounds(row, column)
        # return matrix' cell
        return self[(row * self.columns) + column]
    # end def


    def ensure_inbounds (self, row, column):
        """
            ensures (@row, @column) cell location is actually into
            matrix' bounds; raises IndexError otherwise;
        """
        # out of bounds?
        if not(0 <= row < self.rows and 0 <= column < self.columns):
            # notify error
            raise IndexError(
                "location {} is out of matrix' bounds"
                .format((row, column))
            )
        # end if
    # end def


    def fill_with (self, row, column, **kw):
        """
            hook method to be reimplemented in subclass;
            fills matrix with default items (values or objects);
            this method is called by self.reset_contents();
        """
        # fill matrix with None values
        return None
    # end def


    def get_column_cells (self, column):
        """
            retrieves all @column cells from matrix; will raise
            IndexError if location is out of matrix' bounds;
        """
        # ensure location is in matrix' bounds
        self.ensure_inbounds(0, column)
        # return column cells
        return self[column::self.columns]
    # end def


    def get_columns (self):
        """
            retrieves all columns in matrix, sequentially (from left to
            right);
        """
        # return columns
        return [self[i::self.columns] for i in range(self.columns)]
    # end def


    def get_row_cells (self, row):
        """
            retrieves all @row cells from matrix; will raise IndexError
            if location is out of matrix' bounds;
        """
        # ensure location is in matrix' bounds
        self.ensure_inbounds(row, 0)
        # return row cells
        return self[row * self.columns:(row + 1) * self.columns]
    # end def


    def get_rows (self):
        """
            retrieves all rows in matrix, sequentially (from top to
            bottom);
        """
        # return rows
        return [
            self[i * self.columns:(i + 1) * self.columns]
            for i in range(self.rows)
        ]
    # end def


    def reset (self, **kw):
        """
            resets matrix to fit new @kw keyword arguments;
            supported keywords: rows, columns, fill_with;
        """
        # inits
        self.rows = kw.get("rows") or 0
        self.columns = kw.get("columns") or 0
        _fill_with = kw.get("fill_with")
        # ensure callable
        if callable(_fill_with):
            # preserve subclass hook method overridings this way
            self.fill_with = _fill_with
        # end if
        # must reset contents to reflect changes
        self.reset_contents(**kw)
    # end def


    def reset_contents (self, *args, **kw):
        """
            event handler: resets matrix' contents; fills matrix with
            self.fill_with callable return value;
        """
        # ensure callable
        if not callable(self.fill_with):
            self.fill_with = lambda *args, **kw: None
        # end if
        # clear matrix
        self.clear()
        # fill with default values (could be objects)
        self.extend(
            [
                self.fill_with(_row, _column, **kw)
                for _row in range(self.rows)
                for _column in range(self.columns)
            ]
        )
    # end def

# end class Matrix



class SudokuMatrix (Matrix):
    """
        Generic Sudoku Game matrix model;
        This matrix is a subclass of Python's list class;
        This matrix can be used as a Python list sequence (with some
        additional features);

        Sudoku glossary:

        - a Sudoku GRID is made of ROWS, COLUMNS, BOXES and CELLS;
        - a STACK is made of 3 contiguous vertical BOXES;
        - a BAND is made of 3 contiguous horizontal BOXES;
        - a CHUTE represents either a STACK or a BAND;
        - a UNIT represents a (ROW, COLUMN, BOX) group of CELLS;
        - a GIVEN is an initial given value;
        - a PUZZLE is a partially complete GRID;
        - a PROPER PUZZLE is a GRID with one unique solution;

        Classical Sudoku policies:

        - a Sudoku GRID uses a BASE SEQUENCE of 9 ITEMS e.g. numbers
        from 1 to 9, alphabetical letters or even symbols;
        - each CELL may contain 1 to 9 ITEMS or the Python value None;
        - for historical reasons, ITEMS are frequently called VALUES;
        - a VALUE is always an UNIQUE ITEM into a distinct CELL;
        - to avoid confusion, we choose here to call VALUES unique ITEM
        into SEVERAL CELLS and ITEMS several values into a UNIQUE CELL;
        - each ITEM must appear ONLY ONCE into a given UNIT i.e. only
        once into a given ROW, only once into a given COLUMN and only
        once into a given BOX;
        - to get a PROPER PUZZLE, mathematics have proved there must be
        at least 17 GIVENS into a GRID;
    """

    def __init__ (self, **kw):
        """
            class constructor;
        """
        # member inits
        self.owner = kw.pop("owner", None)
        # default value (1..9)
        self.base_sequence = range(1, 10)
        # super class inits
        super().__init__(**kw)
    # end def


    def __set_cells (self, cells, values, cell_setter):
        """
            private method def for internal use only; sets a given
            group of @cells with data coming from given @values list;
            applies data to cell with @cell_setter attribute;
        """
        # list not empty?
        if values:
            # ensure mutable list
            _list = list(values)
            # browse cells
            for _cell in cells[:min(len(_list), len(cells))]:
                # set value
                exec(
                    "_cell.{attr}(_list.pop(0))"
                    .format(attr=cell_setter)
                )
            # end for
            # update eventual UI display
            self.on_matrix_update()
        # end if
        # return matrix
        return self
    # end def


    def algo_euler_latin_square (self, seed):
        """
            *DEPRECATED* - essentially kept for educational purpose;

            Leonhard Euler's (april 15th, 1707 - sept. 18th, 1783)
            latin square algorithm; takes @seed sequence and builds
            matrix values by rotating left this sequence at each next
            row position; row positions sequence has been slightly
            improved by myself, as I noticed jumping to next relative
            band row position rather than next contiguous row position
            was quite sufficient to comply with Sudoku's third rule:
            all distinct items must appear only once into a box region;

            this algorithm (LERS1) was found on Monday 9th, 2015, in
            about 5 minutes;

            I made this (while rotating left sequence at each step):

                   +--row0          1 2 3 4 5 6 7 8 9   (1)
                +--|--row3<-+       4 5 6 7 8 9 1 2 3       (4)
             +--|--|--row6<-|--+    7 8 9 1 2 3 4 5 6           (7)
             |  |  +->row1  |  |    2 3 4 5 6 7 8 9 1   (2)
             |  +--|->row4  |  |    5 6 7 8 9 1 2 3 4       (5)
             +--|--|->row7  |  |    8 9 1 2 3 4 5 6 7           (8)
             |  |  +->row2--+  |    3 4 5 6 7 8 9 1 2   (3)
             |  +---->row5-----+    6 7 8 9 1 2 3 4 5       (6)
             +------->row8          9 1 2 3 4 5 6 7 8           (9)

            This Euler improved algorithm allows 9! = 362,880 distinct
            playable Sudoku grids; of course, you can mix this with
            matrix vertical / horizontal morphs on chutes and many
            other mixups, but I think simply adding to this a variable
            number of GIVENS for each distinct generated grid would
            probably give hours and hours of pleasant game!
        """
        # ensure mutable list
        _base = list(seed)
        _bl = len(_base)        # nb of items
        _bs = int(_bl**0.5)     # box size = sqrt(_bl)
        # browse rows into a band chute
        for _r0 in range(_bs):
            # browse rows by band-to-band jumps
            for _r1 in range(_bs):
                # set row cells' unique values
                self.set_row_values(
                    _r0 + _r1 * _bs, rotate_left(_base, inplace=True)
                )
            # end for
        # end for
        # return matrix
        return self
    # end def


    def algo_lers2 (self, base_sequence):
        """
            LERS2 algorithm adaptation to fit current class' needs;
            please, see lers2_sudoku_grid() module function def on top
            of this file for more detail;
        """
        # ensure subscriptable
        _base = tuple(base_sequence)
        # nb of items
        _bl = len(_base)
        # box size = sqrt(_bl)
        _bs = int(_bl**0.5)
        # Sudoku chute rectangle area (constant)
        _ca = _bl * _bs
        # browse indexed cells
        for _i, _cell in enumerate(self[:_bl**2]):
            # clear cell and set answer value all at once
            _cell.reset(
                answer=_base[(_i + _bs*(_i//_bl) + _i//_ca) % _bl]
            )
        # end for
        # return matrix
        return self
    # end def


    def algo_shuffle_1 (self):
        """
            Sudoku grid generation shuffle algorithm;
            complexity level 1: does nothing;
        """
        # return matrix
        return self
    # end def


    def algo_shuffle_2 (self):
        """
            Sudoku grid generation shuffle algorithm;
            complexity level 2: shuffles columns into a random stack;
            see class doc for more detail;
        """
        pass                                                                # FIXME
        # return matrix
        return self
    # end def


    def algo_shuffle_3 (self):
        """
            Sudoku grid generation shuffle algorithm;
            complexity level 3: shuffles rows into a random band; see
            class doc for more detail;
        """
        pass                                                                # FIXME
        # return matrix
        return self
    # end def


    def algo_shuffle_4 (self):
        """
            Sudoku grid generation shuffle algorithm;
            complexity level 4: shuffles columns into a random stack
            and rows into a random band; see class doc for more detail;
        """
        # shuffle columns into a random stack
        self.algo_shuffle_2()
        # shuffles rows into a random band
        self.algo_shuffle_3()
        # return matrix
        return self
    # end def


    def algo_shuffle_5 (self):
        """
            Sudoku grid generation shuffle algorithm;
            complexity level 5: shuffles stacks; see class doc for more
            detail;
        """
        pass                                                                # FIXME
        # return matrix
        return self
    # end def


    def algo_shuffle_6 (self):
        """
            Sudoku grid generation shuffle algorithm;
            complexity level 6: shuffles bands; see class doc for more
            detail;
        """
        pass                                                                # FIXME
        # return matrix
        return self
    # end def


    def algo_shuffle_7 (self):
        """
            Sudoku grid generation shuffle algorithm;
            complexity level 7: shuffles stacks and bands; see class
            doc for more detail;
        """
        # shuffle vertical stacks
        self.algo_shuffle_5()
        # shuffle horizontal bands
        self.algo_shuffle_6()
        # return matrix
        return self
    # end def


    def ensure_inbounds_chute (self, index):
        """
            ensures @index is actually into matrix' chute bounds;
            raises IndexError otherwise;
        """
        # out of bounds?
        if not(0 <= index < self.chutes):
            # notify error
            raise IndexError(
                "chute index {} is out of bounds" .format(index)
            )
        # end if
    # end def


    def fill_with (self, row, column, **kw):
        """
            hook method to be reimplemented in subclass; this is called
            by Matrix.reset_contents() super class method;
        """
        # make some overridings
        kw.update(
            owner=self,
            row=row,
            column=column,
            base_sequence=self.base_sequence,
        )
        # fill matrix with cells
        return SudokuMatrixCell(**kw)
    # end def


    def generate (self, level=1):
        """
            generates a Sudoku-compliant fully playable matrix;
            parameter @level allows to choose a level of generation
            complexity (1..7); this generating method uses a Leonhard
            Euler's latin square improved algorithm;
        """
        # set random seed sequence
        _seed = list(self.base_sequence)
        # base seed with 9 items: 9! = 362,880 grid possibilities
        random.shuffle(_seed)
        # set grid answer values
        # + reset cell contents
        # all at once
        self.algo_lers2(_seed)
        # level of complexity management
        try:
            # set matrix' morphs
            exec("self.algo_shuffle_{}()".format(level))
        # unsupported level
        except:
            # warn user
            print(
                "[WARNING]\t*NO* generation algorithm "
                "for complexity level '{}'"
                .format(level)
            )
        # end try
        # relocate cells after shuffling operations
        self.relocate_cells()
        # update eventual UI display
        self.on_matrix_update()
        # return matrix
        return self
    # end def


    def get_answer_values (self):
        """
            gets matrix' cells answer values;
        """
        # get answers
        return [_cell.get_answer_value() for _cell in self]
    # end def


    def get_band (self, index):
        """
            retrieves sequential list of rows corresponding to @index
            given band; raises IndexError if @index is out of bounds;
            see class doc for more detail;
        """
        # ensure inbounds
        self.ensure_inbounds_chute(index)
        # return band' rows
        return [
            # already a Python sequential list
            self.get_row_cells(index * self.chutes + _i)
            for _i in range(self.chutes)
        ]
    # end def


    def get_band_cells (self, index):
        """
            retrieves sequential list of cells corresponding to @index
            given band; raises IndexError if @index is out of bounds;
            see class doc for more detail;
        """
        # inits
        _list = list()
        # browse rows
        for _row in self.get_band(index):
            # fill with row cells
            _list.extend(_row)
        # end for
        # return cells
        return _list
    # end def


    def get_box_cells (self, row, column):
        """
            retrieves all cells of (@row, @column) relied box in
            matrix; see class doc for more detail;
        """
        # ensure location is in matrix' bounds
        self.ensure_inbounds(row, column)
        # inits
        _cells = list()
        # relied box first location
        _bs = int(self.box_size)
        _row0 = int(_bs * (row // _bs))
        _column0 = int(_bs * (column // _bs))
        # browse rows
        for _row in range(_row0, _row0 + _bs):
            # inits
            _index = _row * self.columns + _column0
            # get limited row contents (box size)
            _cells.extend(self[_index:_index + _bs])
        # end for
        # return cells
        return _cells
    # end def


    def get_boxes (self):
        """
            retrieves all boxes in matrix, sequentially (left-to-right
            and top-down); see class doc for more detail;
        """
        # return boxes
        return [
            self.get_box_cells(
                _row * self.box_size, _column * self.box_size
            )
            for _row in range(self.box_size)
            for _column in range(self.box_size)
        ]
    # end def


    def get_stack (self, index):
        """
            retrieves sequential list of columns corresponding to
            @index given stack; raises IndexError if @index is out of
            bounds; see class doc for more detail;
        """
        # ensure inbounds
        self.ensure_inbounds_chute(index)
        # return stack' columns
        return [
            # already a Python sequential list
            self.get_column_cells(index * self.chutes + _i)
            for _i in range(self.chutes)
        ]
    # end def


    def get_stack_cells (self, index):
        """
            retrieves sequential list of cells corresponding to @index
            given stack; raises IndexError if @index is out of bounds;
            see class doc for more detail;
        """
        # inits
        _list = list()
        # browse columns
        for _column in self.get_stack(index):
            # fill with column cells
            _list.extend(_column)
        # end for
        # return cells
        return _list
    # end def


    def get_unit_cells (self, row, column):
        """
            retrieves all surrounding cells for (@row, @column) cell
            location (including this cell) along with Sudoku policies
            compliance e.g. cells in @row row, in @column column and in
            (@row, @column) relied box; Sudoku term for a (row, column,
            box) group of cells is 'unit' or 'scope'; see class doc for
            more detail;
        """
        # return surrounding cells
        return set(
            self.get_row_cells(row)
            + self.get_column_cells(column)
            + self.get_box_cells(row, column)
        )
    # end def


    def on_matrix_update (self, *args, **kw):
        """
            event handler: updates eventual GUI display of matrix; hook
            method to be reimplemented in subclass;
        """
        # put your own code in subclass
        pass
        # debugging
        if __DEBUG__ and __debug__:
            print("\n[DEBUG]\tcurrent matrix state:", self, "\n")
        # end if
        # return matrix
        return self
    # end def


    def relocate_cells (self, *args, **kw):
        """
            event handler: relocates all matrix' cells to fit their
            actual location in matrix e.g. after some shuffling
            operations;
        """
        # inits
        _bl = self.base_len
        # browse cells
        for _i, _cell in enumerate(self):
            # relocate (row, column)
            _cell.relocate(_i // _bl, _i % _bl)
        # end for
        # return matrix
        return self
    # end def


    def reset (self, **kw):
        """
            resets current matrix model; overrides super class method
            def; see class doc for more detail; supported keywords:
            base_sequence, answers, values, show_sieve;
        """
        # inits
        self.base_sequence = tuple(
            kw.get("base_sequence") or self.base_sequence
        )
        self.base_len = len(self.base_sequence)
        # invalid base sequence?
        if not self.base_len:
            # notify error
            raise SudokuMatrixError(
                "invalid base sequence. "
                "Cannot use matrix this way."
            )
        # end if
        # box_size = sqrt(base_len)
        self.box_size = self.base_len**0.5
        # invalid box size?
        if int(self.box_size) != self.box_size:
            # notify error
            raise SudokuMatrixError(
                "invalid sequence length for base sequence. "
                "Cannot determine box size."
            )
        # end if
        # more inits
        self.box_size = int(self.box_size)
        # see class doc for more detail
        # nb of chutes per dimension (horizontally, vertically)
        # chutes = base_len/box_size = n²/n = n = box_size
        self.chutes = self.box_size
        # a Sudoku grid is a square
        self.rows = self.columns = self.base_len
        # reset matrix contents
        self.reset_contents(**kw)
        # set matrix' cells with unique value (or None) for each cell
        # this allows to set up GIVENS on-the-fly
        # see class doc for more detail
        self.set_values(kw.get("values"))
        # set matrix' cells with unique answer value for each cell
        self.set_answer_values(kw.get("answers"))
        # update eventual UI display
        self.on_matrix_update(**kw)
        # return matrix
        return self
    # end def


    def reset_cells (self, **kw):
        """
            resets all matrix' cells with new @kw common keyword args;
            supported common keywords: base_sequence, show_sieve;
        """
        # browse cells
        for _cell in self:
            # reset cell
            _cell.reset(**kw)
        # end for
        # update eventual UI display
        self.on_matrix_update(**kw)
        # return matrix
        return self
    # end def


    def reveal (self, *args, **kw):
        """
            event handler: reveals all answer values in matrix;
        """
        # browse cells
        for _cell in self:
            # reveal answer
            _cell.reveal(*args, **kw)
        # end for
        # update eventual UI display
        self.on_matrix_update(*args, **kw)
        # return matrix
        return self
    # end def


    def set_answer_values (self, answers):
        """
            sets matrix' cells with unique answer value (or None) for
            each cell; answer values are kept hidden unless calling
            self.reveal();
        """
        # internal def
        return self.__set_cells(self, answers, "set_answer_value")
    # end def


    def set_column_values (self, column, values):
        """
            sets unique value (or None) for each cell in @column
            column; will raise SudokuMatrixError if at least one value
            into @values unique value list is not part of base sequence
            or if @column is out of matrix' bounds; see class doc for
            more detail;
        """
        # internal def
        return self.__set_cells(
            self.get_column_cells(column), values, "set_value"
        )
    # end def


    def set_items (self, items):
        """
            sets matrix' cells with multiple items for each cell; see
            class doc for more detail;
        """
        # internal def
        return self.__set_cells(self, items, "set_items")
    # end def


    def set_row_values (self, row, values):
        """
            sets unique value (or None) for each cell in @row row; will
            raise SudokuMatrixError if at least one value into @values
            unique value list is not part of base sequence or if @row
            is out of matrix' bounds; see class doc for more detail;
        """
        # internal def
        return self.__set_cells(
            self.get_row_cells(row), values, "set_value"
        )
    # end def


    def set_values (self, values):
        """
            sets matrix' cells with unique value (or None) for each
            cell; this is useful for setting up GIVENS; see class doc
            for more detail;
        """
        # internal def
        return self.__set_cells(self, values, "set_value")
    # end def


    def show_givens (self, nb):
        """
            shows up @nb givens into matrix' cells; see class doc for
            more detail; minimum number of givens should always be 17;
            raises SudokuMatrixError if @nb < 17;
        """
        # param controls
        if nb < 17:
            # notify error
            raise SudokuMatrixError(
                "to get a PROPER PUZZLE, number of GIVENS "
                "should never be less than 17."
            )
        # end if

        pass                                                                # FIXME

        # update eventual UI display
        self.on_matrix_update()
        # return matrix
        return self
    # end def


    def strip_unit_set_value (self, value, row, column):
        """
            if @value is part of base sequence, strips @value from UNIT
            matrix cells according to Sudoku's game policies i.e.
            strips @value from all cells in @row row, @column column
            and (@row, @column) relied box, except for matrix' cell
            located in (@row, @column) itself, which is set up to this
            unique @value; see class doc for more detail;
        """
        # don't waste your time
        if value in self.base_sequence:
            # browse cells in row, column and relied box (unit)
            for _cell in self.get_unit_cells(row, column):
                # strip value from cell
                _cell.strip_value(value)
            # end for
            # set value for (row, column) cell only
            self.at(row, column).set_value(value)
            # update eventual UI display
            self.on_matrix_update()
        # end if
        # return matrix
        return self
    # end def


    def verify_correct (self):
        """
            returns True if current matrix is fully compliant with all
            Sudoku policies, False otherwise;
        """
        # inits
        _base = set(self.base_sequence)
        _matrix = [_cell.get_value() for _cell in self]
        # verify global harmony
        if set(_matrix) != _base:
            # failed
            return False
        # end if
        # verify more detailed
        _rows = self.rows
        _cols = self.columns
        # browse rows
        for _row in range(_rows):
            # not good?
            if set(_matrix[_row*_cols:(_row+1)*_cols]) != _base:
                # failed
                return False
            # end if
        # end for
        # browse columns
        for _column in range(_cols):
            # not good?
            if set(_matrix[_column::_cols]) != _base:
                # failed
                return False
            # end if
        # end for
        # browse boxes
        for _box in self.get_boxes():
            # not good?
            if set([_c.get_value() for _c in _box]) != _base:
                # failed
                return False
            # end if
        # end for
        # succeeded
        return True
    # end def

# end class SudokuMatrix



class SudokuMatrixCell (list):
    """
        Sudoku matrix cell subcomponent;
        This cell is a subclass of Python's list class;
        This cell can be used as a Python list sequence (with some
        additional features);
        Please, read SudokuMatrix class doc for more detail;
    """

    def __hash__ (self):
        """
            makes this class hashable;
        """
        return id(self)
    # end def


    def __init__ (self, **kw):
        """
            class constructor;
        """
        # super class inits
        super().__init__()
        # member inits
        self.owner = kw.pop("owner", None)
        # default values
        self._answer = None
        self.show_sieve = False
        self.row = self.column = 0
        self.base_sequence = range(1, 10)
        # reset cell
        self.reset(**kw)
    # end def


    def __repr__ (self):
        """
            for debugging session;
        """
        # debug mode?
        if __DEBUG__ and __debug__:
            # too many data to show off?
            if len(self) == len(self.base_sequence):
                # simplify
                return "?"
            # what else?
            else:
                # set digest
                return "".join(map(repr, self))
            # end if
        # NO debug mode
        else:
            # super class representation
            return super().__repr__()
        # end if
    # end def


    def get_answer_value (self):
        """
            returns cell's current answer value; this value should
            always be unique or None;
        """
        return self._answer
    # end def


    def get_value (self):
        """
            returns cell's current value; if cell is still a sequence,
            returns that sequence; otherwise, returns the unique
            contained item itself; if you want to manage cell's inner
            sequence whatever is contained, simply use
            SudokuMatrixCell() itself as a Python list() object;
        """
        # return unique item or sequence otherwise
        return len(self) == 1 and self[0] or self
    # end def


    def on_cell_update (self, *args, **kw):
        """
            event handler: updates eventual GUI display when a matrix'
            cell is modified; hook method to be reimplemented in
            subclass;
        """
        # put your own code in subclass
        pass
    # end def


    def on_unique_value (self, *args, **kw):
        """
            event handler: called when inner value becomes unique; hook
            method to be reimplemented in subclass;
        """
        # put your own code in subclass
        pass
    # end def


    def relocate (self, row, column):
        """
            simply relocates current cell to new (@row, @column) matrix
            location;
        """
        # relocate
        self.row = row
        self.column = column
    # end def


    def reset (self, **kw):
        """
            resets matrix' cell to fit kw args; see SudokuMatrix class
            doc for more detail; supported keywords: row, column,
            answer, base_sequence, show_sieve;
        """
        # inits
        self.solved = False
        self.row = kw.get("row", self.row)
        self.column = kw.get("column", self.column)
        self.base_sequence = tuple(
            kw.get("base_sequence") or self.base_sequence
        )
        self.base_len = len(self.base_sequence)
        self.show_sieve = bool(kw.get("show_sieve", self.show_sieve))
        # set answer value
        self.set_answer_value(kw.get("answer", self._answer))
        # should show sieve in cell?
        if self.show_sieve:
            # show sieve
            self.set_items(self.base_sequence)
        # default behaviour
        else:
            # reset cell to None
            self.set_value(None)
        # end if
    # end def


    def reveal (self, *args, **kw):
        """
            event handler: reveals answer value into cell's inner
            value; *NOT* affected by cell's self.solved locking state;
            returns True if player's single candidate value was
            correct, False in any other case, including answer value is
            None; calls self.on_unique_value() event handler when value
            is in base sequence;
        """
        # get official answer
        _answer = self.get_answer_value()
        # actual answer?
        if _answer is not None:
            # player's answer was correct?
            _response = bool(self.get_value() == _answer)
            # allow updates
            self.solved = False
            # reveal answer
            self.set_value(_answer)
            # cell is now solved (locked)
            self.solved = True
            # return player's answer
            return _response
        # end if
        # invalid answer
        return False
    # end def


    def set_answer_value (self, value):
        """
            sets cell's unique answer value; answer value is kept
            hidden from player's eyes unless self.reveal() is called;
            answer value is *NOT* affected by cell's self.solved
            locking state; raises SudokuMatrixError if @value is not
            part of base sequence or not None (that is, an unregistered
            / unknown value, in fact); see SudokuMatrix class doc for
            more detail;
        """
        # known item?
        if value is None or value in self.base_sequence:
            # set value
            self._answer = value
        # unknown item
        else:
            # notify error
            raise SudokuMatrixError(
                "unknown answer item value '{}'. "
                "Not in base sequence."
                .format(value)
            )
        # end if
    # end def


    def set_items (self, items):
        """
            sets multiple items for cell contents; does nothing if cell
            is locked by self.solved; see SudokuMatrix class doc for
            more detail;
        """
        # allowed to proceed?
        if not self.solved:
            # reset values
            self.clear()
            self.extend(items)
            # update eventual UI display
            self.on_cell_update()
        # end if
    # end def


    def set_value (self, value):
        """
            sets cell's unique value; does nothing if cell is locked by
            self.solved; calls self.on_unique_value() event handler
            when @value is in base sequence; raises SudokuMatrixError
            if @value is not part of base sequence or not None (that
            is, an unregistered / unknown value, in fact);
        """
        # allowed to proceed?
        if not self.solved:
            # None value?
            if value is None:
                # clear inner value
                self.clear()
                self.append(None)
            # known item?
            elif value in self.base_sequence:
                # reset value
                self.clear()
                self.append(value)
                # hook method
                self.on_unique_value()
            # unknown item
            else:
                # notify error
                raise SudokuMatrixError(
                    "unknown cell value '{}'. "
                    "Not in base sequence."
                    .format(value)
                )
            # end if
            # update eventual UI display
            self.on_cell_update()
        # end if
    # end def


    def strip_value (self, value):
        """
            silently removes @value from cell's current sequence; does
            nothing if @value is None or cell is locked by self.solved;
            will call self.on_unique_value() event handler if item left
            after removing is unique; if you want to manage ValueError
            by yourself, simply use SudokuMatrixCell.remove(value) -
            inherited from list.remove(value) - instead;
        """
        # allowed to proceed?
        if not (self.solved or value is None):
            # try out
            try:
                # strip value
                self.remove(value)
            # keep quiet
            except:
                pass
            # keep on trying
            else:
                # got unique value?
                if len(self) == 1:
                    # call hook method (event handler)
                    self.on_unique_value()
                # end if
                # update eventual UI display
                self.on_cell_update()
            # end try
        # end if
    # end def

# end class SudokuMatrixCell



class SudokuMatrixError (Exception):
    """
        Sudoku matrix exception handler;
    """
    pass
# end class SudokuMatrixError



# make some tests
if __name__ == "__main__":
    # get stats
    from statistics import mean
    # get chronometer
    from timeit import timeit
    # stats data inits
    data = list()
    # grid generation test
    matrix = SudokuMatrix()
    # let's make some tests
    for n in range(10):
        # generate grid
        t = timeit(matrix.generate, number=1)
        print("[LERS2] grid generated in: {:0.6f} sec".format(t))
        # add to stats data
        data.append(t)
        # reveal answer
        matrix.reveal()
        # verify: erroneous grid?
        if not matrix.verify_correct():
            print(matrix)
            exit("\n[ERROR] incorrect grid!")
        # end if
    # end for
    print("\n[TOTAL] nb of generated grids:", n + 1)
    print(
        "\n[STATS] average grid generation time: {:0.6f} sec"
        .format(mean(data))
    )
    print("\n[SUCCESS] all grids have been tested OK.")
    data = latin_square()
    print("\n".join(map(str, list(data[i*9:(1+i)*9] for i in range(9)))))
    print("test in {:0.6f} sec".format(timeit(lambda:is_correct_grid(data), number=1)))
    print("grid is correct:", is_correct_grid(data))
# end if
