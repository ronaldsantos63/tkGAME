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

import tkinter as TK

from tkinter import ttk



class GameScore (ttk.Frame):
    r"""
        GameScore - Game subcomponent;
    """

    # default global config values

    CONFIG = {

        "padding": "5px",

    } # end of CONFIG



    def __init__ (self, master=None, **kw):

        # member inits

        self.CONFIG = self.CONFIG.copy()

        self.CONFIG.update(kw)

        # super class inits

        ttk.Frame.__init__(self, master)

        self.configure(**self._only_tk(self.CONFIG))

        # member inits

        self._tk_owner = master

        self._cvar = TK.IntVar()

        # hook method for subclasses

        self.init_widget(**self.CONFIG)

    # end def



    def _bind_high (self, value):
        r"""
            hook method to override in subclass;

            binds score to an upper limit;
        """

        # put your own code in subclass

        # no upper limit by default

        return value

    # end def



    def _bind_low (self, value):
        r"""
            hook method to override in subclass;

            binds score to a lower limit;
        """

        # put your own code in subclass

        # score should *NOT* become negative

        return max(0, value)

    # end def



    def _only_tk (self, kw):
        r"""
            protected method def;

            filters external keywords to suit tkinter init options;

            returns filtered dict() of keywords;
        """

        # inits

        _dict = dict()

        # $ 2014-03-24 RS $
        # Caution:
        # TK widget *MUST* be init'ed before calling _only_tk() /!\
        # self.configure() needs self.tk to work well

        if hasattr(self, "tk") and hasattr(self, "configure"):

            _attrs = set(self.configure().keys()) & set(kw.keys())

            for _key in _attrs:

                _dict[_key] = kw.get(_key)

            # end for

        # end if

        return _dict

    # end def



    def add_score (self, value):
        r"""
            adds value to current score value;
        """

        self._cvar.set(

            self._bind_high(

                self._cvar.get() + abs(int(value))
            )
        )

    # end def



    def get_score (self):
        r"""
            returns current score value;
        """

        return self._cvar.get()

    # end def



    def high_score (self, value):
        r"""
            replaces current score value by @value if greater;
        """

        self._cvar.set(max(self._cvar.get(), int(value)))

    # end def



    def init_widget (self, **kw):
        r"""
            hook method to override in subclass;

            widget's main inits;
        """

        # put your own code in subclass

        self.reset_score()

        # build GUI

        self.score_label = ttk.Label(

            self, text=kw.get("label", "Score:"),

        )

        self.score_label.pack(side=TK.LEFT)

        self.score_display = ttk.Label(

            self, textvariable=self._cvar,

        )

        self.score_display.pack(side=TK.RIGHT)

    # end def



    def reset_score (self):
        r"""
            resets current score value to zero;
        """

        self._cvar.set(0)

    # end def



    def set_score (self, value):
        r"""
            replaces current score value;
        """

        self._cvar.set(int(value))

    # end def



    def sub_score (self, value):
        r"""
            substracts value from current score value;
        """

        self._cvar.set(

            self._bind_low(

                self._cvar.get() - abs(int(value))
            )
        )

    # end def


# end class GameScore
