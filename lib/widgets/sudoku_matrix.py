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
import copy
import math
import random


# module scope function defs

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
        if __debug__:
            # return string representation
            return "{classname} (\n{data}\n)".format(
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
            for _row in range(self.rows // self.box_size)
            for _column in range(self.columns // self.box_size)
        ]
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
        if __debug__:
            print("\n[DEBUG]\tcurrent matrix state:")
            print(self)
            print()
        # end if
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
        # other inits
        self.box_size = math.sqrt(self.base_len)
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
        self.on_matrix_update()
    # end def


    def reset_cells (self, **kw):
        """
            resets all matrix' cells with new common @kw keyword args;
            supported common keywords: base_sequence, show_sieve;
        """
        # browse cells
        for _cell in self:
            # reset cell
            _cell.reset(**kw)
        # end for
        # update eventual UI display
        self.on_matrix_update()
    # end def


    def set_answer_values (self, answers):
        """
            sets matrix' cells with unique answer value for each cell;
            see class doc for more detail;
        """
        # internal def
        self.__set_cells(self, answers, "set_answer_value")
    # end def


    def set_column_values (self, column, values):
        """
            sets unique value for each cell in @column column; will
            raise SudokuMatrixError if at least one value into @values
            unique value list is not part of base sequence or if
            @column is out of matrix' bounds; see class doc for more
            detail;
        """
        # internal def
        self.__set_cells(
            self.get_column_cells(column), values, "set_value"
        )
    # end def


    def set_items (self, items):
        """
            sets matrix' cells with multiple items for each cell; see
            class doc for more detail;
        """
        # internal def
        self.__set_cells(self, items, "set_items")
    # end def


    def set_row_values (self, row, values):
        """
            sets unique value for each cell in @row row; will raise
            SudokuMatrixError if at least one value into @values unique
            value list is not part of base sequence or if @row is out
            of matrix' bounds; see class doc for more detail;
        """
        # internal def
        self.__set_cells(self.get_row_cells(row), values, "set_value")
    # end def


    def set_values (self, values):
        """
            sets matrix' cells with unique value for each cell; see
            class doc for more detail;
        """
        # internal def
        self.__set_cells(self, values, "set_value")
    # end def


    def strip_value (self, value, row, column):
        """
            strips @value from matrix cells according to Sudoku's game
            policies i.e. strips @value from all cells in @row row,
            @column column and (@row, @column) relied box, except for
            matrix cell located in (@row, @column) itself, which is set
            up to this unique @value; see class doc for more detail;
        """
        # browse cells in row, column and relied box (unit)
        for _cell in self.get_unit_cells(row, column):
            # strip value from cell
            _cell.strip_value(value)
            # update eventual UI display
            self.on_matrix_update()
        # end for
        # set value for (row, column) cell only
        self.at(row, column).set_value(value)
        # update eventual UI display
        self.on_matrix_update()
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
        self.answer = None
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
        if __debug__:
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
        return self.answer
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


    def reset (self, **kw):
        """
            resets matrix' cell to fit kw args; see SudokuMatrix class
            doc for more detail; supported keywords: row, column,
            answer, base_sequence, show_sieve;
        """
        # inits
        self.solved = False
        self.row = kw.get("row") or self.row
        self.column = kw.get("column") or self.column
        self.base_sequence = tuple(
            kw.get("base_sequence") or self.base_sequence
        )
        self.base_len = len(self.base_sequence)
        self.show_sieve = bool(kw.get("show_sieve", self.show_sieve))
        # set answer value
        self.set_answer_value(kw.get("answer", self.answer))
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
            value; returns True if player's single candidate value was
            correct, False in any other case, including answer value is
            None; calls self.on_unique_value() event handler when value
            is in base sequence; does nothing if cell is locked by
            self.solved;
        """
        # allowed to proceed?
        if not self.solved:
            # get official answer
            _answer = self.get_answer_value()
            # actual answer?
            if _answer is not None:
                # cell is now solved
                self.solved = True
                # player's answer was correct?
                _response = bool(self.get_value() == _answer)
                # reveal answer
                self.set_value(_answer)
                # return player's answer
                return _response
            # end if
        # end if
        return False
    # end def


    def set_answer_value (self, value):
        """
            sets cell's unique answer value; raises SudokuMatrixError
            if @value is not part of base sequence or not None (unknown
            value); does nothing if cell is locked by self.solved; see
            SudokuMatrix class doc for more detail;
        """
        # allowed to proceed?
        if not self.solved:
            # known item?
            if value is None or value in self.base_sequence:
                # set value
                self.answer = value
            # unknown item
            else:
                # notify error
                raise SudokuMatrixError(
                    "unknown answer item value '{}'. "
                    "Not in base sequence."
                    .format(value)
                )
            # end if
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
        # end if
    # end def


    def set_value (self, value):
        """
            sets cell's unique value; calls self.on_unique_value()
            event handler when @value is in base sequence; raises
            SudokuMatrixError if @value is not part of base sequence or
            not None (unknown value); does nothing if cell is locked by
            self.solved;
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
        # end if
    # end def


    def strip_value (self, value):
        """
            silently removes @value from cell's current sequence; will
            call self.on_unique_value() event handler if last value
            left is unique; does nothing if cell is locked by
            self.solved; if you want to manage ValueError by yourself,
            simply use SudokuMatrixCell.remove(value) instead;
        """
        # allowed to proceed?
        if not self.solved:
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



class SudokuMatrixSolver (SudokuMatrix):
    """
        Sudoku matrix solver class;
        This matrix is a subclass of Python's list class;
        This matrix can be used as a Python list sequence (with some
        additional features);
        Please, read SudokuMatrix class doc for more detail;
    """

    def do_finished (self):
        """
            returns True if matrix is fully solved, False otherwise;
        """
        # browse cells
        for _cell in self:
            # not yet finished?
            if not _cell.solved:
                # abort
                return False
            # end if
        # end for
        # confirm
        return True
    # end def


    def do_solve (self):
        """
            actual matrix' solving loop;
            will raise SudokuMatrixError on failure;
        """
        # inits
        _kw = dict()
        self.step = 1
        # solving loop
        while not self.do_finished():
            # do step task
            exec("self.do_step_{}(_kw)".format(self.step))
            # update eventual GUI display of matrix
            self.on_matrix_update()
        # end while
        # update eventual GUI display of matrix
        self.on_matrix_update()
        #                                                                   FIXME: should verify matrix is correct?
    # end def


    def do_step_1 (self, kw):
        """
            step 1: resets all cells without unique value;
        """
        print("step 1: resetting cells without unique value")
        # browse cells
        for _cell in self:
            # not unique?
            if len(_cell) != 1:
                _cell.reset()
            # unique
            elif not _cell.solved:
                # register for cleanups
                self.register_for_cleanups(_cell)
            # end if
        # end for
        print("end of step 1")
        # go next step
        self.step += 1
    # end def


    def do_step_2 (self, kw):
        """
            step 2: does unique item cleanups in matrix' cells;
        """
        print("step 2: cleanups")
        # loop until no more
        while self.cleanups:
            # get cell
            _cell = self.cleanups.pop()
            print("current cell:", _cell, "len:", len(_cell))
            # may proceed?
            if len(_cell) == 1:
                # lock cell
                _cell.solved = True
                print("stripping value:", _cell.get_value())
                # clean-up values
                self.strip_value(
                    _cell.get_value(), _cell.row, _cell.column
                )
            # end if
        # end while
        print("end of step 2")
        # go next step
        self.step += 1
    # end def


    def do_step_3 (self, kw):
        """
            step 3: makes occurrence simplifications;
        """
        print("step 3: occurrence simplifications")
        # inits
        _sorted = sorted(kw.setdefault("sorted", self), key=len)
        print("sorted matrix:", _sorted)
        # browse cells
        for _cell in _sorted:
            # singleton?
            if len(_cell) == 1:
                # go next cell
                continue
            # low nb of occurrences
            elif len(_cell) <= self.box_size:
                # look up in row, column and box
                _lookups = (
                    "self.get_row_cells(_cell.row)",
                    "self.get_column_cells(_cell.column)",
                    "self.get_box_cells(_cell.row, _cell.column)",
                )
                # browse expressions
                for _expr in _lookups:
                    # get cells
                    _cells = eval(_expr)
                    # look for similar cells
                    _sims = self.get_similar_cells(_cell, _cells)
                    # got similar?
                    if _sims:
                        # add cell itself
                        _sims += (_cell,)
                        # browse cells
                        for _c in _cells:
                            # not a similar?
                            if _c not in _sims:
                                [_c.strip_value(v) for v in _cell]
                            # end if
                        # end for
                    # end if
                # end for
            # too many occurrences
            else:
                # trap out from loop
                break
            # end if
        # end for
        # need to do some cleanups?
        if self.cleanups:
            # go previous step
            self.step -= 1
        # no cleanups
        else:
            # go next step
            self.step += 1
        # end if
        print("end of step 3")
    # end def


    def on_solving_failure (self, *args, exception=None, **kw):
        """
            event handler: notifies user that solving attempt has
            failed; hook method to be reimplemented in subclass; you
            may use this in GUI context;
        """
        # put your own code in subclass
        print("\n[ERROR]\tattempt to solve matrix has *FAILED*.")
        print("\nCaught the following exception:\n")
        print(
            "[{}] {}".format(exception.__class__.__name__, exception)
        )
        print("\nStopped.\n")
        exit(1)
    # end def


    def fill_with (self, row, column, **kw):
        """
            this is called by Matrix.reset_contents() super class
            method;
        """
        # make some overridings
        kw.update(
            owner=self,
            row=row,
            column=column,
            base_sequence=self.base_sequence,
        )
        # fill matrix with cells
        return SudokuMatrixSolverCell(**kw)
    # end def


    def generate (self):
        """
            generates a fully playable solved matrix;
            uses a screened-by resolution algorithm;
        """

                # FIXME: what about Euler's latin square?
                # e.g. rotate_left(_seq) at each row?
                #      + matrix shuffle algos?

        # reset matrix' cell contents
        self.reset_cells()
        # set first row random seed
        _seq = list(self.base_sequence)
        random.shuffle(_seq)
        # browse cells
        for _cell in self.get_row_cells(0): # FIXME: browse rows with self.get_rows()?
                                            # what about self.set_row_values(row, _seq)?
            # set cell value
            _cell.set_value(_seq.pop())
        # end for
        # return solved matrix
        return self
    # end def


    def get_similar_cells (self, cell, cells):
        """
            extracts from @cells only similar cells of @cell;
        """
        return tuple(
            _c for _c in cells if _c == cell and _c is not cell
        )
    # end def


    def register_for_cleanups (self, cell):
        """
            registers @cell for deferred unique item cleanups in
            matrix;
        """
        self.cleanups.add(cell)
    # end def


    def reset (self, **kw):
        """
            resets current matrix model; inherits super class def;
            supported keywords: base_sequence, answers, show_sieve;
        """
        # inits
        self.cleanups = set()
        # make some overridings
        kw.setdefault("show_sieve", True)
        # super class inits
        super().reset(**kw)
    # end def


    def solve (self):
        """
            tries to solve given Sudoku matrix; calls
            self.on_solving_failure() event handler on any exception
            catch; raises SudokuMatrixError if unable to find a
            solution;
        """
        # try out
        try:
            # solving loop
            self.do_solve()
        # failed
        except Exception as e:
            # notify user (event handler)
            self.on_solving_failure(exception=e)
        # end try
    # end def

# end class SudokuMatrixSolver



class SudokuMatrixSolverCell (SudokuMatrixCell):
    """
        Sudoku matrix solver cell subcomponent;
        This cell is a subclass of Python's list class;
        This cell can be used as a Python list sequence (with some
        additional features);
        Please, read SudokuMatrix class doc for more detail;
    """

    def on_unique_value (self, *args, **kw):
        """
            event handler: called when inner value is unique;
            hook method to be reimplemented in subclass;
        """
        # try out
        try:
            # register into solver
            self.owner.register_for_cleanups(self)
        # keep quiet
        except:
            pass
        # end try
    # end def

# end class SudokuMatrixSolverCell



# make some tests
if __name__ == "__main__":
    # ancestor matrix test
    #~ matrix = Matrix()
    # standard matrix test
    matrix = SudokuMatrix()
    # solver test
    matrix = SudokuMatrixSolver()
    print("\nsolved matrix:")
    print(matrix.generate())
# end if
