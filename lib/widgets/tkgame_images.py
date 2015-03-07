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
import os
import os.path as OP
from tkinter import PhotoImage


# module private member
__image_manager = None


# app-wide unique instance getter
def get_image_manager ():
    """
        app-wide unique instance getter
    """
    global __image_manager
    if not isinstance(__image_manager, TkGameImageManager):
        __image_manager = TkGameImageManager()
    # end if
    return __image_manager
# end def


class TkGameImageManager:
    """
        A tkinter.PhotoImage() images manager
    """

    def __init__ (self):
        """
            class constructor
        """
        # member inits
        self.images = dict()
        self.loaded_dirs = list()
    # end def


    def get_image (self, file_path):
        """
            returns the corresponding tkPhotoImage or None, otherwise;
        """
        return self.images.get(file_path)
    # end def


    def get_image_by_name (self, images_dir, name):
        """
            returns the corresponding tkPhotoImage or None, otherwise;
        """
        # inits
        _fname, _fext = OP.splitext(name)
        # return image
        return self.get_image(
            self.get_image_fpath(
                OP.join(images_dir, "{}.gif".format(_fname))
            )
        )
    # end def


    def get_image_fpath (self, filename):
        """
            returns an absolute normalized file path from @filename
            parameter value;
        """
        return OP.abspath(OP.expanduser(filename))
    # end def


    def load_images (self, images_dir, **kw):
        """
            loads images from directory if not previously done;
            optional keywords may be:
            'filter_callback': filters image file path to
                determine if it should be taken or not; will look
                for GIF image files if omitted;
            'recursive': boolean to browse images_dir recursively;
                no recursion by default, if omitted;
        """
        # inits
        images_dir = OP.abspath(OP.expanduser(images_dir))
        # not already done?
        if images_dir not in self.loaded_dirs:
            # callback inits
            filter_cb = kw.get("filter_callback") or self.is_gif
            # browse directory
            for _file in os.listdir(images_dir):
                _file = OP.abspath(OP.join(images_dir, _file))
                # not in collection?
                if _file not in self.images:
                    if OP.isdir(_file):
                        if kw.get("recursive"):
                            self.load_images(_file, **kw)
                        # end if
                    elif filter_cb(_file):
                        self.images[_file] = PhotoImage(file=_file)
                    # end if
                # end if
            # end for
            # directory has been loaded OK
            self.loaded_dirs.append(images_dir)
        # end if
    # end def


    def is_gif (self, file_path):
        """
            determines if file_path ends with a '.gif' file extension
            or not; this feature is case-insensitive;
        """
        return file_path.lower().endswith(".gif")
    # end def

# end class TkGameImageManager
