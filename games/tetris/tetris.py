#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    tkGAME - all-in-one Game library for Tkinter

    TetrisGame - Generic Tetris Game

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

import tkRAD

# debugging session
#~ tkRAD.i18n.switch_off()



class TetrisGame (tkRAD.RADApplication):
    r"""
        TetrisGame - Generic Tetris Game
    """

    APP = {

        "name": _("Tetris"),

        "version": _("0.1a"),

        "description": _("Tetris - Generic Tetris Game"),

        "title": _("Tetris"),

        "author": _("Raphaël SEBAN <motus@laposte.net>"),

        "copyright": _("(c) 2014+ Raphaël SEBAN <motus@laposte.net>"),

        "license_short": _(
            "This project is licensed under the GNU "
            "General Public License v3.\n"
            "Please, see http://www.gnu.org/licenses/ "
            "for more detail."
        ),

        "license": _(
            "This program is free software: you can redistribute it"
            "and/or modify it under the terms of the GNU General"
            "Public License as published by the Free Software"
            "Foundation, either version 3 of the License, or (at your"
            "option) any later version.\n"

            "This program is distributed in the hope that it will be"
            "useful, but WITHOUT ANY WARRANTY; without even the"
            "implied warranty of MERCHANTABILITY or FITNESS FOR A"
            "PARTICULAR PURPOSE. See the GNU General Public License"
            "for more details.\n"

            "You should have received a copy of the GNU General Public"
            "License along with this program.\n"

            "If not, see: http://www.gnu.org/licenses/"
        ),

        "license_url": _("http://www.gnu.org/licenses/"),

    } # end of APP



    DIRECTORIES = (

        "src", "locale", "xml",

    ) # end of DIRECTORIES



    PYTHON = {

        "version": "3.2",

        "strict": False,

    } # end of PYTHON



    RC_OPTIONS = {

        "user_file": "user_options.rc",

        "user_dir": "~/.config/tkgame/tetris",

        "app_file": "app.rc",

        "app_dir": "^/etc",

    } # end of RC_OPTIONS



    def _start_gui (self, **kw):

        from src import mainwindow as MW

        self.mainwindow = MW.MainWindow(**kw)

        self.mainwindow.run()

    # end def

# end class TetrisGame



# launching game

if __name__ == "__main__":

    # launch app

    TetrisGame().run()

# end if
