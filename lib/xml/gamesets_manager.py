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

import xml.etree.ElementTree as ET



# subcomponent class def

class XMLGameset:
    r"""
        XMLGameset - GamesetsManager subcomponent;
    """

    # main member inits

    DOCTYPE = "gameset"

    ELEMENT_BUILDER = "_build_element_{xml_tag}"

    ATTRIBUTE_PARSER = "_parse_attribute_{xml_attr}"



    def __init__ (self, filepath):

        # member inits

        self.filepath = filepath

        self.xml_tree = None

    # end def



    def _build_element (self, xml_element, parent, **kw):
        r"""
            builds one XML element as object;
        """

        if self.cast_xml_element(xml_element):

            _xml_tag = kw.get("xml_tag", xml_element.tag)

            _builder = getattr(

                self,

                str(self.ELEMENT_BUILDER).format(xml_tag=_xml_tag),

                None
            )

            if callable(_builder):

                # call XML element builder

                _builder(xml_element, parent, **kw)

            else:

                raise AttributeError(

                    "invalid XML element builder for <{xml_tag}>"

                    .format(xml_tag=_xml_tag)
                )

            # end if

        # end if

    # end def



    def _parse_xml_attributes (self, xml_element, parent, **kw):
        r"""
            parses one XML element's XML attributes;
        """

        if self.cast_xml_element(xml_element):

            _xml_attrs = kw.get("xml_attrs", xml_element.attrib)

            for _xml_attr, _value in _xml_attrs.items():

                _parser = getattr(

                    self,

                    str(self.ATTRIBUTE_PARSER)
                        .format(xml_attr=_xml_attr),

                    None
                )

                # XML attribute parsing is optional

                if callable(_parser):

                    # update keywords

                    kw.update(
                        parent=parent,
                        xml_element=xml_element,
                        xml_attr=_xml_attr,
                        xml_attrs=_xml_attrs,
                    )

                    # call XML attribute parser

                    _parser(_value, **kw)

                # end if

            # end for

        # end if

    # end def



    def cast_xml_element (self, xml_element):
        r"""
            tries to determine if @xml_element is of ET.Element type;

            raises TypeError otherwise;

            returns True on success, False otherwise;
        """

        # param controls

        if ET.iselement(xml_element):

            # success

            return True

        # type mismatch

        else:

            raise TypeError(

                "XML element must be of '{obj_type}' type"

                .format(obj_type=repr(ET.Element))
            )

            # failure

            return False

        # end if

    # end def



    def xml_build (self):
        r"""
            builds a gameset along XML file defs;
        """

        # init objects collection

        self.objects = dict()

        # load XML defs

        self.xml_tree = ET.parse(self.filepath)

        # get root XML element

        _root = self.xml_tree.getroot()

        # got correct doctype?

        if _root and _root.tag == self.DOCTYPE:

            # start building

            self._build_element(_root, self)

        else:

            raise TypeError(

                "root node should be of type <{doctype}>"

                .format(doctype=self.DOCTYPE)
            )

        # end if

    # end def


# end class XMLGameset



class GamesetsManager:
    r"""
        Generic Gameset collection manager;
    """

    def __init__ (self, main_dir="xml/gamesets", file_ext="xml", gameset=XMLGameset):

        # member inits

        self.gamesets = dict()

        self.gameset = gameset

        self.current_gameset = "default"

        self.main_dir = main_dir

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



    @property
    def gameset (self):
        r"""
            returns gameset class type to use;
        """

        return self.__gameset

    # end def



    @gameset.setter
    def gameset (self, value):

        if issubclass(value, XMLGameset):

            self.__gameset = value

        else:

            raise TypeError(

                "Gameset must be of type 'XMLGameset' or subclass"
            )

        # end if

    # end def



    @gameset.deleter
    def gameset (self):

        del self.__gameset

    # end def



    def get_current_gameset (self):
        r"""
            returns the current gameset, if exists;

            raises KeyError otherwise;
        """

        return self.gamesets[self.current_gameset]

    # end def



    def get_gameset (self, name):
        r"""
            returns a gameset along name, if exists;

            raises KeyError otherwise;
        """

        return self.gamesets[name]

    # end def



    def init_gameset (self, filepath):
        r"""
            creates a new gameset along its XML file defs;
        """

        _gameset = self.gameset(filepath)

        _gameset.xml_build()

        return _gameset

    # end def



    def load_gamesets (self, main_dir=None):
        r"""
            tries to load gamesets from @main_dir;

            uses internal self.main_dir if @main_dir is *NOT* a
            correct directory;
        """

        # param inits

        main_dir = self.normalize_path(main_dir)

        # param controls

        if not OP.isdir(main_dir):

            main_dir = self.main_dir

        # end if

        # get files list

        _files = glob.glob(OP.join(main_dir, "*" + self.file_ext))

        # loop on files

        for _file in _files:

            _name = OP.splitext(OP.basename(_file))[0]

            self.gamesets[_name] = self.init_gameset(_file)

        # end for

    # end def



    @property
    def main_dir (self):
        r"""
            returns current main directory;
        """

        return self.__main_dir

    # end def



    @main_dir.setter
    def main_dir (self, value):

        # param inits

        value = self.normalize_path(value)

        # param controls

        if self.cast_dir(value):

            # set new value

            self.__main_dir = value

        # end if

    # end def



    @main_dir.deleter
    def main_dir (self):

        del self.__main_dir

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



    def set_current_gameset (self, name):
        r"""
            sets the current gameset, if exists in self.gamesets;

            raises KeyError otherwise;
        """

        if self.get_gameset(name):

            self.current_gameset = name

        # end if

    # end def


# end class GamesetsManager
