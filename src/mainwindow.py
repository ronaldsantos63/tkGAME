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

from tkinter import messagebox as MB

import tkRAD



class MainWindow (tkRAD.RADXMLMainWindow):
    r"""
        application's main window;
    """

    def init_widget (self, **kw):
        r"""
            main window's inits;
        """

        # init menu

        self.topmenu.xml_build()

        # init GUI

        self.mainframe.xml_build()

        # connect statusbar

        self.connect_statusbar("show_statusbar")

        # connect events

        self.events.connect_dict(
            {
                "MenuHelpAbout": self._show_about_dialog,
            }
        )

    # end def



    def _show_about_dialog (self, *args, **kw):
        r"""
            tkRAD event slot method;
            shows off 'About...' dialog box;
        """

        # show 'About...' dialog box

        MB.showinfo(

            _("About"),

            "{name} v{version}\n\n"

            "{description}\n\n"

            "Copyright {copyright}\n\n"

            "{license_short}"

            .format(**self.app.APP),

            parent=self,
        )

    # end def


# end class MainWindow
