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

import os

import tkinter as TK

from tkinter import ttk



class ScrollView (ttk.Frame):
    r"""
        Generic Scrollable Viewport;
    """

    def __init__ (self, master=None, **kw):
        r"""
            class constructor;
        """

        # super class inits

        super().__init__(master)

        self.configure(**self._only_tk(kw))

        # member inits

        self.tk_owner = master

        self.platform = os.name.lower()

        # widget inits

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



    def _slot_container_changed (self, tkevent=None, *args, **kw):
        r"""
            viewport's frame container has changed (size, ...);
        """

        self._update_scrollregion()

    # end def



    def _slot_mouse_wheel (self, tk_event=None, *args, **kw):
        r"""
            generic handler for <MouseWheel> tkEvent;
        """

        # MS-Windows specifics

        if self.platform == "nt":

            _step = -tk_event.delta // 120

        # Apple MacOS specifics

        elif self.platform == "mac":

            _step = -tk_event.delta

        # other POSIX / UNIX-like

        else:

            _step = (tk_event.num == 5) - (tk_event.num == 4)

        # end if - platform

        # do vertical scrollings

        self.viewport.yview_scroll(_step, "units")

    # end def



    def _slot_viewport_changed (self, tkevent=None, *args, **kw):
        r"""
            viewport canvas has changed (size, others...);
        """

        self._update_scrollregion()

    # end def



    def _update_scrollregion (self):
        r"""
            updates canvas' scrollregion along contents;
        """

        self.viewport.configure(scrollregion=self.viewport.bbox(TK.ALL))

    # end def



    def init_widget (self, **kw):
        r"""
            widget main inits;
        """

        # canvas inits

        self.viewport = TK.Canvas(self)

        # widgets container inits

        self.container = ttk.Frame(self.viewport)

        self.container_id = self.viewport.create_window(

            0, 0, anchor=TK.NW, window=self.container,
        )

        # scrollbar inits

        self.scrollbar_x = ttk.Scrollbar(self, orient=TK.HORIZONTAL)

        self.scrollbar_y = ttk.Scrollbar(self, orient=TK.VERTICAL)

        # connecting scrollbars

        self.viewport.configure(

            xscrollcommand=self.scrollbar_x.set,

            yscrollcommand=self.scrollbar_y.set,
        )

        self.scrollbar_x.configure(command=self.viewport.xview)

        self.scrollbar_y.configure(command=self.viewport.yview)

        # window sizegrip inits

        self.sizegrip = ttk.Sizegrip(self)

        # layout inits

        self.viewport.grid(row=0, column=0, sticky=TK.NW+TK.SE)

        self.scrollbar_x.grid(row=1, column=0, sticky=TK.E+TK.W)

        self.scrollbar_y.grid(row=0, column=1, sticky=TK.N+TK.S)

        self.sizegrip.grid(row=1, column=1)

        # make resizable

        self.rowconfigure(0, weight=1)

        self.columnconfigure(0, weight=1)

        # bind tkevents

        self.viewport.bind("<Configure>", self._slot_viewport_changed)

        self.container.bind("<Configure>", self._slot_container_changed)

        for _seq in ("<Button-4>", "<Button-5>", "<MouseWheel>"):

            self.bind_all(_seq, self._slot_mouse_wheel)

        # end for

    # end def


# end class ScrollView



# demo sample

def demo ():

    root = TK.Tk()

    scrollview = ScrollView(root, padding=5)

    scrollview.pack(expand=1, fill=TK.BOTH)

    for i in range(10):

        TK.Label(

            scrollview.container,

            text="Hello good people!",

            font="sans 24 bold",

        ).pack(padx=10, pady=20, expand=1, fill=TK.BOTH)

    # end for

    root.mainloop()

# end def



# example

if __name__ == "__main__":

    demo()

# end if
