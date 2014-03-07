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

from tkRAD.widgets.rad_frame import RADFrame



class GameSectionBrowser (RADFrame):
    r"""
        tkGAME section browser compound object class;
    """

    def init_widget (self, **kw):
        r"""
            widget inits;
        """

        # inits - see class defs below

        self.navbar = GameSectionNavBar(self)

        self.view = GameSectionView(self)

        self.navbar.pack(expand=0, fill=TK.X)

        self.view.pack(expand=1, fill=TK.BOTH)

        # connect events

        self.events.connect_dict(
            {
                "NamedEvent": None,
            }
        )

    # def end


# end class



class GameSectionNavBar (RADFrame):
    r"""
        tkGAME game section browser subcomponent (navigation bar);
    """

    def init_widget (self, **kw):
        r"""
            widget inits;
        """

        TK.Label(self, text="debug:NavBar", bg="yellow").pack(**self.PACK_OPTIONS)

    # end def


# end class GameSectionNavBar



class GameSectionView (RADFrame):
    r"""
        tkGAME game section browser subcomponent (data view);
    """

    def init_widget (self, **kw):
        r"""
            widget inits;
        """

        TK.Label(self, text="debug:View", bg="red").pack(**self.PACK_OPTIONS)

    # end def


# end class GameSectionView
