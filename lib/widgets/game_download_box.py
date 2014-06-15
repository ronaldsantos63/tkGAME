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

import urllib.request as WEB

import tkRAD

from tkRAD.core import tools

from tkRAD.core import path as P



class GameDownloadBox (tkRAD.RADXMLFrame):
    r"""
        Web remote file downloader dialog box class;
    """



    def _cancel_download (self, tk_event=None, *args, **kw):
        r"""
            cancelling pending download operation;
        """

        # cancelled OK

        self.events.raise_event(

            "GameDownloadBoxCancelled", widget=self,
        )

    # end def



    def _display_url (self, url=""):
        r"""
            displays URL in a short way;
        """

        _cvar = self.get_stringvar("remote_url")

        if _cvar:

            _cvar.set(P.shorten_path(url, limit=64))

        # end if

    # end def



    def _update_progressbar (self, block_count, block_size, file_size):
        r"""
            updates progressbar value along params;
        """

        #~ print("update progressbar:", block_count, block_size, file_size)

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

        self.update_idletasks()

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

        self._display_url(url)

        # update display

        self.events.raise_event(

            "GameDownloadBoxStart", widget=self,
        )

        # clean up temp files

        WEB.urlcleanup()

        to_file, _headers = WEB.urlretrieve(

            url, to_file, reporthook=self._update_progressbar
        )

        self.events.raise_event(

            "GameDownloadBoxDone", widget=self,
        )

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
                    textvariable="remote_url"
                    foreground="blue"
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
                    <ttkbutton
                        name="button_cancel"
                        text="Cancel"
                        command="@GameDownloadBoxCancel"
                        layout="grid"
                        layout_options="row=0, column=2, padx=5"
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

        # progressbar inits

        self.reset()

        # connecting people

        self.events.connect(

            "GameDownloadBoxCancel", self._cancel_download
        )

    # end def



    def reset (self, tk_event=None, *args, **kw):
        r"""
            resets components to initial state;
        """

        self._update_progressbar(0, 0, 0)

        self._display_url()

    # end def


# end class GameDownloadBox
