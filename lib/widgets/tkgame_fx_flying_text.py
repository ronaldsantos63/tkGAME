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

import math
import tkinter.constants as TK
from . import tkgame_animations as AP


class TkGameFXFlyingText:
    """
        Game special effects:
        canvas flying text along (curve(x), curve(y)) functions;
    """

    def __init__ (self, canvas):
        """
            class constructor
        """
        # member inits
        self.canvas = canvas
        self.animations = AP.get_animation_pool()
        self.colors = dict()
        self.shadow = None
        self.cid_text = 0
        self.cid_shadow = 0
        self.x0, self.y0 = (0, 0)
    # end def


    def animation_loop (self, x, y, ratio_x, ratio_y, frame=0):
        """
            special effects animation loop;
        """
        # curve functions
        try:
            x = self.curve_x(ratio_x * frame)
            y = self.curve_y(ratio_y * frame)
        except:
            #~ print("exception on curve calculations")
            pass
        else:
            # update display
            _x, _y = (self.x0 + x, self.y0 - y)
            if self.shadow:
                rx, ry, color = self.shadow
                self.canvas.coords(self.cid_shadow, _x + rx, _y + ry)
                self.canvas.itemconfigure(
                    self.cid_shadow, fill=self.get_shadow_color(frame)
                )
            # end if
            self.canvas.coords(self.cid_text, _x, _y)
            self.canvas.itemconfigure(
                self.cid_text, fill=self.get_text_color(frame)
            )
        # end try
        # should keep on animating?
        if frame < self.frames:
            # update frame
            frame += 1
            # loop again
            self.animations.run_after(
                self.delay, self.animation_loop,
                x, y, ratio_x, ratio_y, frame
            )
        # animation ended
        else:
            # stop all!
            self.stop()
        # end if
    # end def


    def create_text (self, x, y, **options):
        """
            same as canvas.create_text(x, y, **options);
            admits optional shadow=(rx, ry, color);
        """
        # inits
        self.x0, self.y0 = (x, y)
        self.colors["text"] = options.get("fill")
        self.shadow = options.pop("shadow", None)
        self.cid_shadow = 0
        # shadow feature asked?
        if self.shadow:
            # inits
            rx, ry, color = self.shadow
            self.colors["shadow"] = color
            s_opts = options.copy()
            s_opts.update(fill=color)
            # create shadow text
            self.cid_shadow = self.canvas.create_text(
                x + rx, y + ry, **s_opts
            )
        # end if
        # create text
        self.cid_text = self.canvas.create_text(x, y, **options)
        # set text above all
        self.canvas.tag_raise(self.cid_shadow, TK.ALL)
        self.canvas.tag_raise(self.cid_text, TK.ALL)
    # end def


    def fx_cos (self, amplitude=1, offset=0):
        """
            closure for cosinusoidal curve f(x) = a * cos(x + b);
        """
        return lambda x: amplitude * math.cos(x + offset)
    # end def


    def fx_hyperbolic (self, numerator=1, offset=0):
        """
            closure for hyperbolic curve f(x) = a / (x + b);
        """
        return lambda x: numerator / (x + offset)
    # end def


    def fx_linear (self, coeff=1, offset=0):
        """
            closure for linear curve f(x) = a * (x + b);
        """
        return lambda x: coeff * (x + offset)
    # end def


    def fx_log10 (self, amplitude=1, offset=0):
        """
            closure for base-10 logarithmic curve
            f(x) = a * log10(x + b);
        """
        return lambda x: amplitude * math.log10(x + offset)
    # end def


    def fx_ln (self, amplitude=1, offset=0):
        """
            closure for natural logarithmic curve f(x) = a * ln(x + b);
        """
        return lambda x: amplitude * math.log(x + offset)
    # end def


    def fx_quadratic (self, amplitude=1, offset=0):
        """
            closure for quadratic curve f(x) = a * (x + b)**2;
        """
        return lambda x: amplitude * (x + offset)**2
    # end def


    def fx_sin (self, amplitude=1, offset=0):
        """
            closure for sinusoidal curve f(x) = a * sin(x + b);
        """
        return lambda x: amplitude * math.sin(x + offset)
    # end def


    def get_callback (self, *callbacks):
        """
            returns the first callable callback function if found;
            raises an exception FXFlyingTextError otherwise;
        """
        for _cb in callbacks:
            if callable(_cb):
                return _cb
            # end if
        # end for
        raise FXFlyingTextError(
            "unable to get a callable callback function."
        )
    # end def


    def init_kw (self, **kw):
        """
            member keyword inits;
        """
        # keyword inits
        self.keep_alive = bool(kw.get("keep_alive"))
        self.delay = kw.get("delay") or 50
        self.vector = kw.get("vector") or (0, 100)
        self.frames = kw.get("frames") or 20
        self.curve_x = self.get_callback(
            kw.get("curve_x"), self.fx_linear()
        )
        self.curve_y = self.get_callback(
            kw.get("curve_y"), self.fx_linear()
        )
        self.get_text_color = self.get_callback(
            kw.get("get_text_color"), self.text_color
        )
        self.get_shadow_color = self.get_callback(
            kw.get("get_shadow_color"), self.shadow_color
        )
    # end def


    def on_animation_end (self, *args, **kw):
        """
            hook method to be reimplemented in subclass;
            manages the end of a given animation loop;
        """
        # drop text from canvas
        self.canvas.delete(self.cid_shadow)
        self.canvas.delete(self.cid_text)
    # end def


    def shadow_color (self, frame):
        """
            retrieves shadow color along @frame value;
            hook method to be reimplemented in subclass;
        """
        return self.colors.get("shadow")
    # end def


    def start (self, **kw):
        """
            starts animation loop on demand;
        """
        # param inits
        self.init_kw(**kw)
        # got something to animate?
        if self.cid_text:
            # inits
            vx, vy = self.vector
            ratio_x = vx / self.frames
            ratio_y = vy / self.frames
            # run animation loop
            self.animations.run_after(
                self.delay, self.animation_loop, 0, 0, ratio_x, ratio_y
            )
        # no text by there!
        else:
            # error
            raise FXFlyingTextError(
                "no text to animate. "
                "Please, use {0}.create_text() method "
                "to set up some animated text "
                "before calling {0}.start() method."
                .format(__class__.__name__)
            )
        # end if
    # end def


    def stop (self, *args, **kw):
        """
            stops animation loop on demand;
        """
        # stop eventual loop
        self.animations.stop(self.animation_loop)
        # call hook method
        if not self.keep_alive:
            self.on_animation_end()
        # end if
    # end def


    def text_color (self, frame):
        """
            retrieves text color along @frame value;
            hook method to be reimplemented in subclass;
        """
        return self.colors.get("text")
    # end def

# end class TkGameFXFlyingText



class FXFlyingTextError (Exception):
    """
        exception handler for class TkGameFXFlyingText;
    """
    pass

# end class FXFlyingTextError
