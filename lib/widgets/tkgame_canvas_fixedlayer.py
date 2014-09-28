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


# private module member
__fixed_layer = None


# app-wide unique instance getter
def get_fixed_layer (canvas):
    """
        retrieves app-wide unique instance of animation pool
    """
    global __fixed_layer
    if not isinstance(__fixed_layer, TkGameCanvasFixedLayer):
        __fixed_layer = TkGameCanvasFixedLayer(canvas)
    # end if
    return __fixed_layer
# end def


class TkGameCanvasFixedLayer:
    """
        Viewport fixed layer for text canvas items (tkinter);
    """

    def __init__ (self, canvas):
        """
            class constructor
        """
        # member inits
        self.canvas = canvas
        self.objects = dict()
    # end def


    def add (self, *canvas_id):
        """
            adds multiple canvas item ids to objects dictionary;
        """
        # loop on list
        for _cid in canvas_id:
            # add new item
            self.add_coords(_cid)
        # end for
    # end def


    def add_coords (self, canvas_id, *coords):
        """
            adds canvas item id with @coords to objects dictionary;
        """
        # param inits
        if not coords:
            coords = self.canvas.coords(canvas_id)
        # end if
        # add canvas item by id
        self.objects[canvas_id] = coords
    # end def


    def clear (self):
        """
            clears up objects dict;
        """
        self.objects.clear()
    # end def


    def remove (self, *canvas_id):
        """
            removes canvas item ids from objects dictionary;
        """
        # loop on items
        for _cid in canvas_id:
            # silent drops
            self.objects.pop(_cid, None)
        # end for
    # end def


    def update_positions (self, *args, **kw):
        """
            generic event handler;
            updates positions of all registered canvas items;
        """
        # loop on objects collection
        for canvas_id, coords in self.objects.items():
            # init new coords
            _new = []
            # loop on coordinates
            for i in range(0, len(coords), 2):
                _new.append(self.canvas.canvasx(coords[i]))
                _new.append(self.canvas.canvasy(coords[i + 1]))
            # end for
            # update positions
            self.canvas.coords(canvas_id, *_new)
        # end for
    # end def

# end class TkGameCanvasFixedLayer
