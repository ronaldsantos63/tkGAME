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

# launching game

if __name__ == "__main__":

    # launch app

    #~ TetrisGame().run()

    import tkinter.messagebox as MB

    if MB.askquestion("Question", "Quit normally?") == MB.YES:

        print("Program exited OK.")

        exit(0)

    else:

        raise SystemError("Ouch! I feel so sick !")

    # end if

# end if
