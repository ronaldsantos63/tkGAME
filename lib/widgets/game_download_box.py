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
import concurrent.futures as ASYNC

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

        return GameDownloadBox(tk_owner, **kw).download(url, to_file)

    # must show in dialog window

    else:

        # dialog window inits

        return GameDownloadDialog(tk_owner, **kw).download(url, to_file)

    # end if

# end def



# ===========================   CLASS DEF   ============================



class GameDownloadBox (tkRAD.RADXMLFrame):
    r"""
        Web remote file downloader dialog box class;
    """



    def _cancel_download (self, tk_event=None, *args, **kw):
        r"""
            cancelling pending download operation;
        """

        # try to cancel thread

        self.thread.cancel()

        # cancelled OK

        self.events.raise_event(

            "GameDownloadBoxCancelled", widget=self,
        )

    # end def



    def _update_progressbar (self, block_count, block_size, file_size):
        r"""
            updates progressbar value along params;
        """

        # param inits

        _bcount = tools.ensure_int(block_count)

        _bsize = tools.ensure_int(block_size)

        _fsize = tools.ensure_int(file_size)

        # do we know file size?

        if _fsize > 0:

            # update options

            _options = dict(

                mode="determinate",

                maximum=_fsize,

                value=_bcount * _bsize,
            )

            self.progressbar.stop()

        # indeterminate file size

        else:

            # update options

            _options = dict(

                mode="indeterminate",

                maximum=10,

                value=0,
            )

            self.progressbar.start()

        # end if

        # update progressbar

        self.progressbar.configure(orient="horizontal", **_options)

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

        # display some info

        self.label_url.configure(

            text=P.shorten_path(url, limit=64),
        )

        # update display

        self.update_idletasks()

        # clean up temp files

        WEB.urlcleanup()

        # set async procedure

        with ASYNC.ThreadPoolExecutor(max_workers=1) as executor:

            # back to the future!

            self.thread = executor.submit(

                WEB.urlretrieve,

                url,

                filename=to_file,

                reporthook=self._update_progressbar,
            )

            # get return values

            try:

                # return values for WEB.urlretrieve()

                to_file, _headers = self.thread.result()

            except Exception as e:

                # reset file path

                to_file = None

                # display some info

                self.label_url.configure(

                    text="Error: {}".format(str(e)),

                    foreground="red",
                )

                raise

            # end try

        # end with

        return to_file

    # end def



    def init_widget (self, **kw):
        r"""
            widget main inits;
        """

        # internal XML source code (overridable)

        _xml = """
            <tkwidget>
                <ttklabel
                    text="Downloading:"
                    layout="pack"
                    resizable="width"
                />
                <ttklabel
                    name="label_url"
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
                        command="@GameDownloadBoxCancel"
                        layout="grid"
                        layout_options="row=0, column=2"
                    />
                </ttkframe>
            </tkwidget>
        """

        # build GUI

        self.xml_build(

            tools.choose_str(

                kw.get("filename"), kw.get("xml"), _xml,
            )
        )

        # force progressbar to be horizontal

        self._update_progressbar(0, 0, 0)

        # connecting people

        self.events.connect(

            "GameDownloadBoxCancel", self._cancel_download
        )

    # end def


# end class GameDownloadBox



# ===========================   CLASS DEF   ============================



class GameDownloadDialog (DLG.RADDialog):
    r"""
        Web remote file downloader dialog window class;
    """



    def _slot_download_cancelled (self, tk_event=None, *args, **kw):
        r"""
            tries to quit dialog;
        """

        self._slot_pending_task_off()

        self._slot_quit_dialog(tk_event, *args, **kw)

    # end def



    def download (self, url, to_file=None):
        r"""
            tries to download file from @url into @to_file or into a
            temp file if omitted;

            returns target file path;
        """

        to_file = self.container.download(url, to_file)

        self.show()

        return to_file

    # end def



    def init_widget (self, **kw):
        r"""
            widget main inits;
        """

        self.set_contents(GameDownloadBox(self, **kw))

        self.events.connect(

            "GameDownloadBoxCancelled", self._slot_download_cancelled
        )

    # end def


# end class GameDownloadDialog
