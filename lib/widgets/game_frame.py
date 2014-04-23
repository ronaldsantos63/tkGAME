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

from tkinter import ttk



class GameFrame (ttk.Frame):
    r"""
        Generic game frame component;
    """


    def __init__ (self, master=None, **kw):

        # super class inits

        ttk.Frame.__init__(self, master)

        self.configure(**self._only_tk(kw))

        # member inits

        self.tk_owner = master

        # set widget contents

        self.init_widget(**kw)

    # end def



    def _only_tk (self, kw):
        r"""
            protected method def;

            filters external keywords to suit tkinter init options;

            returns filtered dict() of keywords;
        """

        # inits

        _dict = dict()

        # $ 2014-02-24 RS $
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



    def init_widget (self, **kw):
        r"""
            this should be overridden in subclass;
        """

        # put here your own code in subclass

        pass

    # end def


# end class GameFrame
