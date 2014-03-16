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

import os.path as OP

import urllib.request as WEB

import tkinter as TK

import tkRAD

from tkRAD.core import tools

#~ import tkRAD.widgets.rad_dialog_window as DLG



# module function def

def download (url, to_file=None, tk_owner=None, **kw):
    r"""
        tries to download file set in @url, put it in @to_file and
        shows progressbar in dialog box;
    """

    # only a subcomponent?

    if isinstance(tk_owner, (TK.Frame, TK.ttk.Frame)):

        # get file download box

        _box = GameFileDownloadBox(tk_owner, **kw)

    # must show in dialog window

    else:

        # dialog window inits

        _dlg = GameFileDownloadDialog(tk_owner, **kw)

        # get file download box

        _box = _dlg.get_download_box()

    # end if

    return _box.download(url, to_file)

# end def



class GameFileDownloadBox (tkRAD.RADXMLFrame):
    r"""
        Web remote file downloader dialog box class;
    """

    def init_widget (self, **kw):
        r"""
            widget main inits;
        """

        # XML source code inits

        _xml = """
            <tkwidget>
                <ttklabel
                    text="Downloading:"
                    layout="pack"
                    resizable="width"
                />
                <ttklabel
                    textvariable="remote_url"
                    padding="0px 3px"
                    layout="pack"
                    resizable="width"
                />
                <ttkframe
                    layout="pack"
                    resizable="width"
                >
                    <ttkprogressbar
                        name="progressbar"
                        length="5cm"
                        maximum="10"
                        mode="indeterminate"
                        orient="horizontal"
                        layout="grid"
                        layout_options="row=0, column=0"
                        resizable="width"
                    />
                    <ttkframe
                        width="5"
                        layout="grid"
                        layout_options="row=0, column=1"
                    />
                    <ttkbutton
                        text="Cancel"
                        command="@GameFileDownloadBoxCancel"
                        layout="grid"
                        layout_options="row=0, column=2"
                    />
                </ttkframe>
            </tkwidget>
        """

        # build GUI

        _source = tools.choose_str(

            kw.get("filename"),

            kw.get("xml"),

            _xml,
        )

        self.xml_build(_source)

        self.configure(padding="5px")

        _cvar = self.get_stringvar("remote_url")

        _cvar.set("say captain, say what, say captain, say what, say captain, say what you want?")

        # make some animations

        self.progressbar.start()

        # connecting people :)

        self.events.connect(

            "GameFileDownloadBoxCancel", self._cancel_download
        )

    # end def



    def download (self, url, to_file=None):
        r"""
            tries to download file from @url into @to_file or into a
            temp file if omitted;

            returns target file path;
        """

        print("download: FIXME!")

        return to_file

    # end def



    def _cancel_download (self, *args, **kw):
        r"""
            cancelling pending download operation;
        """

        print("cancel download asked!")

    # end def

# end class GameFileDownloadBox



# FIXME: should be a tkRAD.widgets.RADDialogWindow

class GameFileDownloadDialog (TK.Toplevel):
    r"""
        Web remote file downloader dialog window class;
    """

    def __init__ (self, master=None, **kw):

        # super class inits

        super().__init__()

        # transient parent inits

        self.transient(master)

        # WM protocol inits

        self.protocol("WM_DELETE_WINDOW", self._close_dialog)

        # other inits

        self.resizable(width=False, height=False)

        self.minsize(width=20, height=20)

        # widget inits

        self.__download_box = GameFileDownloadBox(self, **kw)

        self.__download_box.pack()

    # end def



    def _close_dialog (self, *args, **kw):

        print("close dialog!")

        self.destroy()

    # end if



    def get_download_box (self):
        r"""
            returns private file download box subcomponent;
        """

        return self.__download_box

    # end def


# end class GameFileDownloadDialog
