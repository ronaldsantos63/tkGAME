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

from tkinter import messagebox as MB



class GameApplication (TK.Tk):
    r"""
        Generic Tkinter game application main window;
    """

    # main member inits

    PADDING = 10    # pixels



    def __init__ (self, **kw):

        # super class inits

        TK.Tk.__init__(self)

        # prevent from accidental displaying

        self.withdraw()

        # member inits

        self.title("My Game")

        self.protocol("WM_DELETE_WINDOW", self.quit_app)

        self.resizable(width=False, height=False)

        # widget inits

        self.init_widget(**kw)

        # emergency trap

        self.bind_all("<Control-Escape>", self.quit_app)

    # end def



    def center_window (self, *args, **kw):
        r"""
            tries to center window along screen dims;

            no return value (void);
        """

        # ensure dims are correct

        self.update_idletasks()

        # window size inits

        _width = self.winfo_reqwidth()

        _height = self.winfo_reqheight()

        _screen_width = self.winfo_screenwidth()

        _screen_height = self.winfo_screenheight()

        # make calculations

        _left = (_screen_width - _width) // 2

        _top = (_screen_height - _height) // 2

        # update geometry

        self.geometry("+{x}+{y}".format(x=_left, y=_top))

    # end def



    def init_widget (self, **kw):
        r"""
            this should be overridden in subclass;
        """

        # put your own code in subclass

        # inits

        _pad = self.PADDING

        # component inits

        self.canvas = TK.Canvas(self, bg="black", width=300, height=400)

        self.canvas.pack(side=TK.TOP, padx=_pad, pady=_pad)

        # quit button

        ttk.Button(

            self, text="Quit", command=self.quit_app,

        ).pack(side=TK.RIGHT, padx=_pad, pady=_pad)

        # events handler

        self.bind_all("<Escape>", self.quit_app)

    # end def



    def quit_app (self, *args, **kw):
        r"""
            quit app dialog;
        """

        # ask before actually quitting

        if MB.askokcancel("Question", "Quit game?", parent=self):

            self.quit()

        # end if

    # end def



    def run (self, *args, **kw):
        r"""
            actually runs the game;
        """

        # show up window

        self.center_window()

        self.deiconify()

        # hook method

        self.start_game(**kw)

        # enter the loop

        self.mainloop()

    # end def



    def start_game (self, *args, **kw):
        r"""
            hook method - this should be overridden in subclass;
        """

        # put your own code in subclass

        print("Starting game now!")

    # end def


# end class GameApplication



# launching the game app

if __name__ == "__main__":

    GameApplication().run()

# end if
