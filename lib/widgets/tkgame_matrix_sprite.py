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

# mandatory dependencies
from . import tkgame_canvas_sprite as CS
from . import tkgame_matrix as MX


class TkGameMatrixSprite (CS.TkGameCanvasSprite):
    """
        A sprite is an animated graphical object that manages
        several states such as wait, walk, run, jump, etc;
    """

    def __init__ (self, owner, matrix, canvas, **kw):
        """
            class constructor
        """
        # inits
        _kw = kw.copy()
        _kw.update(subclassed=True)
        # super class inits
        super().__init__(owner, canvas, **_kw)
        # member inits
        self.matrix = matrix
        self.row_column = (kw.get("row") or 0, kw.get("column") or 0)
        # for best simplification - hook method
        if not kw.get("subclassed"):
            self.init_sprite(**kw)
        # end if
    # end def


    def destroy (self, *args, **kw):
        """
            event handler for sprite destruction;
            should be reimplemented in subclass;
        """
        # stop animations
        super().destroy(*args, **kw)
        # delete from matrix
        self.matrix.drop_xy(self.xy)
    # end def


    def look_ahead (self, sx, sy):
        """
            looks around current sprite to see who might collide;
            this overrides super class function def;
        """
        # inits
        rel_xy = (sx * self.matrix.cellsize, sy * self.matrix.cellsize)
        # look ahead
        sprite = self.matrix.rel_at_xy(self.xy, rel_xy)
        # return data
        return {"sprite": sprite, "rel_xy": rel_xy, "sx": sx, "sy": sy}
    # end def


    @property
    def matrix (self):
        """
            game matrix attribute;
            must be of TkGameMatrix type;
        """
        return self.__matrix
    # end def

    @matrix.setter
    def matrix (self, value):
        """
            game matrix attribute;
            must be of TkGameMatrix type;
        """
        if isinstance(value, MX.TkGameMatrix):
            self.__matrix = value
        else:
            raise TypeError(
                "'matrix' attribute must be of "
                "'TkGameMatrix' type or at least a subclass of this."
            )
        # end if
    # end def

    @matrix.deleter
    def matrix (self):
        del self.__matrix
    # end def


    def move_animation (self, c_dict):
        """
            here is the animation of a moving sprite;
            this overrides super class function def;
        """
        # moving is quite simple here
        # but you can reimplement this in your own subclasses
        dx, dy = c_dict["rel_xy"]
        # relative move on canvas
        self.canvas.move(self.canvas_id, dx, dy)
        # update matrix
        self.matrix.rel_move_xy(self.xy, (dx, dy))
        # update pos
        self.x += dx
        self.y += dy
    # end def


    @property
    def row_column (self):
        """
            sprite's (row, column) location on matrix;
        """
        return self.matrix.row_column(self.xy)
    # end def

    @row_column.setter
    def row_column (self, value):
        # inits
        self.xy = self.matrix.center_xy(value)
    # end def

# end class TkGameMatrixSprite
