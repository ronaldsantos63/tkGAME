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

import re

import glob

import os.path as OP

import tkinter as TK



class PhotoStock:
    r"""
        Generic Tkinter.PhotoImage collection manager;
    """

    def __init__ (self, images_dir="images", file_ext="gif"):

        # member inits

        self.images = dict()

        self.images_dir = images_dir

        self.file_ext = file_ext

    # end def



    def cast_dir (self, dirpath):
        r"""
            casts @dirpath to determine if it is a correct directory
            path;

            raises OSError otherwise;
        """

        # param controls

        if OP.isdir(dirpath):

            # succeeded

            return True

        else:

            raise NotADirectoryError(

                "'{path}' is *NOT* a valid directory path."

                .format(path=dirpath)
            )

            # failed

            return False

        # end if

    # end def



    @property
    def file_ext (self):
        r"""
            returns current available file extension;
        """

        return self.__file_ext

    # end def



    @file_ext.setter
    def file_ext (self, value):

        self.__file_ext = (

            "." + re.sub(r"\W+", r"", str(value))

        ).rstrip(".")

    # end def



    @file_ext.deleter
    def file_ext (self):

        del self.__file_ext

    # end def



    def get_image (self, name):
        r"""
            returns a Tkinter.PhotoImage along name, if exists;

            returns None otherwise;
        """

        return self.images.get(name)

    # end def



    @property
    def images_dir (self):
        r"""
            returns current images main directory;
        """

        return self.__images_dir

    # end def



    @images_dir.setter
    def images_dir (self, value):

        # param inits

        value = self.normalize_path(value)

        # param controls

        if self.cast_dir(value):

            # set new value

            self.__images_dir = value

        # end if

    # end def



    @images_dir.deleter
    def images_dir (self):

        del self.__images_dir

    # end def



    def load_images (self, images_dir=None):
        r"""
            tries to load PhotoImages from @images_dir;

            uses internal self.images_dir if @images_dir is *NOT* a
            correct directory;

            returns True on success, False otherwise;
        """

        # param inits

        images_dir = self.normalize_path(images_dir)

        # param controls

        if not OP.isdir(images_dir):

            images_dir = self.images_dir

        # end if

        # get files list

        _files = glob.glob(OP.join(images_dir, "*" + self.file_ext))

        # loop on files

        for _file in _files:

            _name = OP.splitext(OP.basename(_file))[0]

            self.images[_name] = TK.PhotoImage(file=_file)

        # end for

    # end def



    def normalize_path (self, path):
        r"""
            normalizes @path along with current OS constraints;
        """

        if path and isinstance(path, str):

            return OP.normcase(

                OP.normpath(

                    OP.abspath(

                        OP.realpath(

                            OP.expanduser(path)
                        )
                    )
                )
            )

        else:

            return ""

        # end if

    # end def


# end class PhotoStock
