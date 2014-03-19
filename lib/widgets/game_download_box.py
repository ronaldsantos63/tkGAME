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

from tkRAD.core import path as P

import tkRAD.widgets.rad_dialog as DLG



# module function def

def download (url, to_file=None, tk_owner=None, **kw):
    r"""
        tries to download file set in @url, put it in @to_file and
        shows progressbar in dialog box;

        returns target file path;
    """

    # only a subcomponent?

    if isinstance(tk_owner, (TK.Frame, TK.ttk.Frame)):

        # get file download box

        _box = GameDownloadBox(tk_owner, **kw)

        return _box.download(url, to_file)

    # must show in dialog window

    else:

        # dialog window inits

        _dlg = GameDownloadDialog(tk_owner, **kw)

        return _dlg.download(url, to_file)

    # end if

# end def



# ===========================   CLASS DEF   ============================



class GameDownloadBox (tkRAD.RADXMLFrame):
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
                        name="button"
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

        # make some animations

        self.progressbar.start()

        # connecting people

        self.events.connect(

            "GameDownloadBoxCancel", self._cancel_download
        )

    # end def



    def download (self, url, to_file=None):
        r"""
            tries to download file from @url into @to_file or into a
            temp file if omitted;

            returns target file path;
        """

        # param controls

        if not tools.is_pstr(url):

            raise TypeError(

                _("expected plain string of chars in URL parameter.")
            )

            return None

        # end if

        if tools.is_pstr(to_file):

            to_file = P.normalize(to_file)

        # end if

        # stop animations

        self.progressbar.stop()

        self.progressbar.configure(mode="determinate")

        # display some info

        _cvar = self.get_stringvar("remote_url")

        _cvar.set(P.shorten_path(url, limit=64))

        # process inits

        self.target_path = to_file

        self.source_url = url

        # ===================================================================FIXME

        # 'resume' download from start

        self._resume_download()

        return self.target_path

    # end def



    def _resume_download (self, tk_event=None, *args, **kw):
        r"""
            resuming interrupted download process;
        """

        print("resume download", tk_event, args, kw)

        self.button.configure(

            text=_("Cancel"),

            command=self._cancel_download,
        )

        self.events.raise_event(

            "GameDownloadBoxResumingNow", widget=self,
        )

    # end def



    def _cancel_download (self, tk_event=None, *args, **kw):
        r"""
            cancelling pending download operation;
        """

        print("cancel download asked!", tk_event, args, kw)

        self.button.configure(

            text=_("Resume"),

            command=self._resume_download,
        )

        self.events.raise_event(

            "GameDownloadBoxCancellingNow", widget=self,
        )

    # end def


# end class GameDownloadBox



# ===========================   CLASS DEF   ============================



class GameDownloadDialog (DLG.RADButtonsDialog):
    r"""
        Web remote file downloader dialog window class;
    """



    def _slot_button_abandon (self, tk_event=None, *args, **kw):
        r"""
            tries to quit dialog;
        """

        self._slot_quit_dialog(tk_event, *args, **kw)

    # end def



    def init_widget (self, **kw):
        r"""
            widget main inits;
        """

        self.set_contents(GameDownloadBox(self, **kw))

        self.set_buttons("Abandon")

    # end def



    def download (self, url, to_file=None):
        r"""
            tries to download file from @url into @to_file or into a
            temp file if omitted;

            returns target file path;
        """

        self._slot_pending_task_on()

        to_file = self.container.download(url, to_file)

        self.show()

        return to_file

    # end def


# end class GameDownloadDialog
