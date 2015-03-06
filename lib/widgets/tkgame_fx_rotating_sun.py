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
import math
import cmath
import tkinter.constants as TK
from . import tkgame_animations as AP



class TkGameFXRotatingSun:
    """
        Game special effects: rotating sun;
    """

    # class constant defs
    TAGORID = "rotating"


    def __del__ (self):
        """
            class destructor;
        """
        self.stop()
    # end def


    def __init__ (self, canvas, **kw):
        """
            class constructor;
        """
        self.canvas = canvas
        self.animations = AP.get_animation_pool()
        self.bgcolor = kw.get("bgcolor") or "royalblue3"
        self.fgcolor = kw.get("fgcolor") or "dodgerblue3"
        self.life_cycle = kw.get("life_cycle")  # in ms
        self.nb_rays = kw.get("nb_rays") or 6
        self.angle = kw.get("angle") or 1       # in degrees
        self.delay = kw.get("delay") or 50      # in ms
        self.origin = None
    # end def


    def animation_loop (self, angle, delay):
        """
            rotating solar rays animation loop;
        """
        # inits
        x0, y0 = self.origin
        # rotate all coords
        for _id in self.canvas.find_withtag(self.TAGORID):
            self.canvas.coords(
                _id,
                *self.rotate_coords(
                    self.canvas.coords(_id), x0, y0, angle
                )
            )
        # end for
        # schedule loop again
        self.animations.run_after(
            delay, self.animation_loop, angle, delay
        )
    # end def


    def draw (self):
        """
            draws rotating sun game FX;
        """
        # clear canvas
        self.canvas.delete(TK.ALL)
        # set background color
        self.canvas.configure(bg=self.bgcolor)
        # inits
        cw = self.canvas.winfo_reqwidth()
        ch = self.canvas.winfo_reqheight()
        cx, cy = cw//2, ch//2
        self.origin = x0, y0 = (cx, ch)
        radius = 1.2 * abs(complex(x0, y0))
        omega = 2 * math.pi / self.nb_rays
        point = lambda n, phi=0: (
            x0 + radius * math.cos(n * omega + phi),
            y0 + radius * math.sin(n * omega + phi)
        )
        # ray tracing
        for n in range(self.nb_rays):
            x1, y1 = point(n)
            x2, y2 = point(n, omega/2)
            self.canvas.create_polygon(
                x1, y1, x0, y0, x2, y2,
                fill=self.fgcolor,
                tags=self.TAGORID,
            )
        # end for
        # rising sun
        radius = cy//2
        self.canvas.create_oval(
            x0 - radius * 1.5, y0 - radius + 20,
            x0 + radius * 1.5, y0 + radius + 20,
            fill=self.fgcolor,
            width=0,
        )
    # end def


    def rotate_coords (self, coords, x0, y0, angle):
        """
            rotates set of coords along origin (x0, y0) and angle;
        """
        _coords = []
        for i in range(0, len(coords), 2):
            x, y = coords[i], coords[i + 1]
            r, phi = cmath.polar(complex(x - x0, y - y0))
            z = cmath.rect(r, phi + angle)
            _coords.extend([x0 + z.real, y0 + z.imag])
        # end for
        return _coords
    # end def


    def start (self, delay=None, angle=None):
        """
            starts animation loop;
        """
        # ensure drawn at least once
        if not self.origin:
            self.draw()
        # end if
        # inits
        delay = delay or self.delay or 50
        angle = angle or self.angle or 1
        # start animation loop
        self.animations.run_after(
            1, self.animation_loop, math.radians(angle), delay
        )
        # stop after life cycle
        if self.life_cycle:
            self.animations.run_after(self.life_cycle, self.stop)
        # end if
    # end def


    def stop (self, *args, **kw):
        """
            event handler: stops animation loop;
        """
        # stop animation loop
        self.animations.stop(self.animation_loop)
    # end def

# end class TkGameFXRotatingSun
