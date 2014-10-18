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
from . import tkgame_animations as AP
from . import tkgame_events as EM


class TkGameBaseWidget:
    """
        TkGame abstract base widget to use in subclasses;
        Works only when coupled with a tkinter widget class in
        subclass;
    """

    # predefined options
    CONFIG = dict(
    )


    def _only_tk (self, kw):
        """
            protected method def;
            filters external keywords to suit tkinter init options;
            returns filtered dict() of keywords;
        """
        # inits
        _dict = dict()
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


    def _safe_init (self, tkclass, master=None, **options):
        """
            subclass safe initializer;
        """
        # option inits
        _opts = self.CONFIG.copy()
        _opts.update(**options)
        # super class inits
        tkclass.__init__(self, master)
        self.configure(**self._only_tk(_opts))
        # member inits
        self.animations = AP.get_animation_pool()
        self.events = EM.get_event_manager()
        # widget inits
        self.init_widget(**_opts)
    # end def


    def center_xy (self):
        """
            returns (x, y) coordinates of widget's central point;
        """
        return (self.winfo_reqwidth() / 2, self.winfo_reqheight() / 2)
    # end def


    def classname (self):
        """
            returns instance's class name;
        """
        return self.__class__.__name__
    # end def


    def init_widget (self, **kw):
        """
            hook method to be reimplemented in subclass;
        """
        pass
    # end def


    def size (self):
        """
            returns (reqwidth(), reqheight()) of tk widget;
        """
        return (self.winfo_reqwidth(), self.winfo_reqheight())
    # end def

# end class TkGameBaseWidget
