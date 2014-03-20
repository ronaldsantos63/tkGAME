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

import os.path as OP

from tkinter import messagebox as MB

import tkRAD

from tkRAD.core import path as P

from tkRAD.core import tools

import lib.widgets.game_download_box as DNL



class MainWindow (tkRAD.RADXMLMainWindow):
    r"""
        Gabe application's main window class;
    """



    def __download_package (self, item_attrs):
        r"""
             tries to download zip archive and install it locally;
        """

        # inits

        _src = item_attrs["src"]

        # got remote zip archive?

        if tools.is_pstr(_src):

            # ask user for downloading zip archive

            _response = MB.askquestion(

                _("Download"),

                _(
                    "Package is missing locally.\n"
                    "Download it from the web?"
                ),

                parent=self,
            )

            # user is OK to download package

            if _response == MB.YES:

                # show download box component

                self._show_download_box()

                # download in temporary file

                _tempfile = self.mainframe.download_box_frame.download(

                    url=_src, to_file="^/tmp/archive.zip"
                )

                print("mainwindow::temp_file:", _tempfile)

                # TODO: verify ZIP archive

                # TODO: unzip archive into target package dir

                # TODO: run script if OK

            else:

                MB.showinfo(
                    _("Info"),

                    _("Package download aborted."),

                    parent=self,
                )

            # end if - MB.response

        else:

            # error

            raise ValueError(

                _("no remote ZIP archive to download")
            )

        # end if - _src

    # end def



    def __get_item_attrs (self, xml_element):
        r"""
            trying to retrieve item's specific XML attributes;
        """

        # get attrs dict

        _attrs = {

            # main: python executable

            "main": tools.choose_str(

                xml_element.get("main"),

                "main.py",
            ),

            # package: game/editor own directory

            "package": tools.choose_str(

                xml_element.get("package"),

                "misc",
            ),

            # src: remote zip archive

            "src": tools.choose_str(

                xml_element.get("src"),
            ),

            # type: 'game' or 'editor'

            "type": tools.choose_str(

                xml_element.get("type"),

                "game",
            ),

            # target directories

            "dirs": {

                "game": "^/games",

                "editor": "^/editors",
            },

        } # end of attrs dict

        # build package dir path

        _attrs["package_dir"] = P.normalize(

            OP.join(

                _attrs["dirs"].get(_attrs["type"]),

                _attrs["package"],
            )
        )

        # build executable script path

        _attrs["exe_path"] = OP.join(

            _attrs["package_dir"], _attrs["main"]
        )

        return _attrs

    # end def



    def __open_item (self, xml_element):
        r"""
            trying to open game/editor along with XML attrs;
        """

        # param controls

        if self.mainframe.cast_element(xml_element):

            # inits

            _attrs = self.__get_item_attrs(xml_element)

            # package installed?

            if OP.isdir(_attrs["package_dir"]):

                # try to run "main" executable

                self.__run_script(_attrs)

            else:

                # ask for download

                self.__download_package(_attrs)

        # end if - xml_element

    # end def



    def __run_script (self, item_attrs):
        r"""
             tries to launch executable Python script;
        """

        # inits

        _exe_path = item_attrs["exe_path"]

        print("running script:", _exe_path)

    # end def



    def _hide_download_box (self, tk_event=None, *args, **kw):
        r"""
            hides download box component;
        """

        self.mainframe.download_box_frame.grid_remove()

        self.mainframe.download_box_frame.reset()

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



    def _show_download_box (self, tk_event=None, *args, **kw):
        r"""
            shows download box component;
        """

        self.mainframe.download_box_frame.grid()

        self.update()

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

                    "to open an item:\n\n{error}"

                ).format(error=str(e)),

                parent=self,
            )

            # FIXME: report error to remote DB?
            #~ apport(...???...)
            raise

        finally:

            self._hide_download_box()

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

        # ensure download box is hidden

        self.mainframe.download_box_frame.button_cancel.grid_forget()

        self._hide_download_box()

        # run game section browser

        self.mainframe.game_section_browser.show("local_sections")

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

    # end def

# end class MainWindow
