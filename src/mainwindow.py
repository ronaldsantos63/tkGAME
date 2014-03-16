#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    tkGAME - all-in-one Game library for Tkinter

    Gabe - Game Browser

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

from tkRAD.core import tools



class MainWindow (tkRAD.RADXMLMainWindow):
    r"""
        Gabe application's main window class;
    """



    def __open_item (self, xml_element):
        r"""
            trying to open game/editor along with XML attrs;
        """

        # param controls

        if self.mainframe.cast_element(xml_element):

            # inits

            # main: python executable

            _main = tools.choose_str(

                xml_element.get("main"),

                "main.py",
            )

            # src: remote zip archive

            _src = tools.choose_str(

                xml_element.get("src"),
            )

            # type: 'game' or 'editor'

            _type = tools.choose_str(

                xml_element.get("type"),

                "game",
            )

            print("main:", _main, "src:", _src, "type:", _type)

        # end if - xml_element

    # end def



    def _show_about_dialog (self, *args, **kw):
        r"""
            tkRAD event slot method;
            shows off 'About...' dialog box;
        """

        # show 'About...' dialog box

        MB.showinfo(

            _("About"),

            ("{name} v{version}\n\n"

            "{description}\n\n"

            "Copyright {copyright}\n\n"

            "{license_short}"

            ).format(**self.app.APP),

            parent=self,
        )

    # end def



    def _slot_mouse_scrolldown (self, *args, **kw):
        r"""
            raises tkRAD event instead;
        """

        self.events.raise_event("MouseWheelScrollDown", *args, **kw)

    # end def



    def _slot_mouse_scrollup (self, *args, **kw):
        r"""
            raises tkRAD event instead;
        """

        self.events.raise_event("MouseWheelScrollUp", *args, **kw)

    # end def



    def _slot_open_item (self, *args, **kw):
        r"""
            tries to open a game editor executable, first looks
            locally then looks on the web for dnl/installing if
            missing locally;
        """

        try:

            self.__open_item(kw.get("xml_element"))

        except Exception as e:

            MB.showerror(

                _("Error"),

                _(
                    "An error has occurred while trying "

                    "to open an item:\n{error}"

                ).format(error=str(e)),

                parent=self,
            )

            # FIXME: report error to remote DB?
            #~ apport(...???...)

        # end try

    # end def



    def init_widget (self, **kw):
        r"""
            main window's inits;
        """

        # init menu - default is ^/xml/menu/topmenu.xml

        self.topmenu.xml_build()

        # init GUI - default is ^/xml/widget/mainwindow.xml

        self.mainframe.xml_build()

        # connect statusbar to stringvar control variable

        self.connect_statusbar("show_statusbar")

        # connect tkRAD simplified events

        self.events.connect_dict(
            {
                "MenuHelpAbout": self._show_about_dialog,

                "StatusBarInfo": self.statusbar.info,

                "StatusBarNotify": self.statusbar.notify,

                "GameSectionBrowserOpenSection": None,          # TODO?

                "GameSectionBrowserOpenItem": self._slot_open_item,
            }
        )

        # bind tkevents

        self.bind_all("<Button-4>", self._slot_mouse_scrollup)

        self.bind_all("<Button-5>", self._slot_mouse_scrolldown)

        # run game section browser

        self.mainframe.game_section_browser.show("local_sections")

    # end def

# end class MainWindow
