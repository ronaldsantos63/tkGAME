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

import os.path as OP

import urllib.request as WEB


import tkinter as TK

import tkinter.messagebox as MB


import tkRAD

from tkRAD.core import tools

from tkRAD.core import path as P

from tkRAD.widgets.rad_frame import RADFrame


from .game_scroll_view import GameScrollView



class GameSectionBrowser (RADFrame):
    r"""
        tkGAME section browser compound object class;
    """

    def init_widget (self, **kw):
        r"""
            widget inits;
        """

        # inits - see class defs below

        self.navbar = GameSectionNavBar(self)

        self.view = GameSectionView(self)

        # layout inits

        self.navbar.pack(expand=0, fill=TK.X)

        self.view.pack(expand=1, fill=TK.BOTH)

        # connect events

        self.events.connect_dict(
            {
                "GameSectionNavBarGoHome": self.view.go_home,

                "GameSectionNavBarGoParent": self.view.go_parent,
            }
        )

    # def end



    def show (self, filename=None, *args, **kw):
        r"""
            shows off section browser with its contents filled up;
        """

        # delayed build along with web mirrors data

        self.after(100, self.view.web_build, filename, *args, **kw)

        # do *NOT* wait after HTTP response

        self.update_idletasks()

    # end def

# end class



class GameSectionNavBar (tkRAD.RADXMLFrame):
    r"""
        tkGAME game section browser subcomponent (navigation bar);
    """

    def init_widget (self, **kw):
        r"""
            widget inits;
        """

        # build GUI

        self.xml_build(self._get_xml_source())

    # end def



    def _get_xml_source (self, *args, **kw):
        r"""
            virtual method to be overridden in subclasses;
        """

        return """
            <tkwidget>
                <button
                    text="Home"
                    image="^/images/browser/home.gif"
                    compound="left"
                    relief="flat"
                    command="@GameSectionNavBarGoHome"
                    layout="pack"
                    layout_options="side='left'"
                />
                <button
                    text="Go to parent"
                    image="^/images/browser/go_parent.gif"
                    compound="left"
                    relief="flat"
                    command="@GameSectionNavBarGoParent"
                    layout="pack"
                    layout_options="side='left'"
                />
            </tkwidget>
        """

    # end def

# end class GameSectionNavBar



class GameSectionView (GameScrollView):
    r"""
        tkGAME game section browser subcomponent (data view);
    """

    # default XML attrs
    # overrides RADXMLWidget.ATTRS

    ATTRS = {

        "common": {

            "id": None,
            "image": "unknown",
            "compound": TK.TOP,
            "font": "sans 10 bold",
            "relief": TK.FLAT,
            "offrelief": TK.FLAT,
            "width": "200",
            "height": "180",
            "wraplength": "180",
            "layout": "pack",
            "layout_options": "side='left'",
            "resizable": "yes",
        },

        "group": {

            "layout_options": "side='top'",
        },

        "item": {

            "command": "._open_item",
            "main": "main.py",
            "package": "misc",
            "src": None,
            "text": "Game",
            "type": "game",
        },

        "section": {

            "command": "._open_section",
            "text": "Section",
        },

    } # end of ATTRS

    # XML tree root element
    # overrides RADXMLBase.DOCTYPE

    DOCTYPE = "tksection"

    # accepted XML child elements for XML container element

    DTD = {

        "group": ("section", "item"),

        "item": ("none", ),

        "section": ("section", "item", "group"),

        "tksection": ("section", "item", "group"),

    } # end of DTD

    # Images dir and fallback

    IMAGES_DIR = "^/images/section"

    IMAGE_UNKNOWN = "unknown.gif"

    # XML file path parts for xml_build() automatic mode
    # overrides RADXMLWidget.XML_RC

    XML_RC = {

        # expects ^/xml/data/tkgame_sections.xml
        # as DEFAULT XML file

        "dir": "^/xml/data",

        "filename": "tkgame_sections",

        "file_ext": ".xml",

        "mirror_url": "https://raw.github.com/tarball69/tkGAME/master",

    } # end of XML_RC



    def _build_element_group (self, xml_tag, xml_element, tk_parent):
        r"""
            building <group> root element;
        """

        # generic view item

        self._build_view_item(xml_tag, xml_element, tk_parent)

    # end def



    def _build_element_item (self, xml_tag, xml_element, tk_parent):
        r"""
            building <item> XML element;
        """

        # generic view item

        self._build_view_item(xml_tag, xml_element, tk_parent)

    # end def



    def _build_element_section (self, xml_tag, xml_element, tk_parent):
        r"""
            building <section> XML element;
        """

        # generic view item

        self._build_view_item(xml_tag, xml_element, tk_parent)

    # end def



    def _build_element_tksection (self, xml_tag, xml_element, tk_parent):
        r"""
            building <tksection> root element;
        """

        # param controls

        if self.cast_parent(tk_parent):

            # loop on XML element children

            return self._loop_on_children(

                xml_element, tk_parent, accept = self.DTD.get(xml_tag),
            )

        # end if

        # failure

        return False

    # end def



    def _build_view_item (self, xml_tag, xml_element, tk_parent):
        r"""
            protected method def;

            builds any view item along the same widget;

            returns True on build success, False otherwise;
        """

        # param controls

        if self.cast_element(xml_element):

            # attr inits

            _attributes = self._init_deferred_attributes(

                xml_tag, xml_element, tk_parent
            )

            # widget inits

            _widget = self.get_object_by_id(_attributes.get("id"))

            if not _widget:

                # item group?

                if xml_tag == "group":

                    # new widget

                    _widget = TK.Frame(tk_parent)

                else:

                    # new widget

                    _widget = TK.Radiobutton(

                        tk_parent,

                        # mandatory attrs (not overridable)

                        indicatoron=0,

                        variable=self._cvar,

                        value=_attributes.get("id"),
                    )

                # end if

                # $ 2014-03-11 RS $
                # since tkRAD v1.4: deferred tasks
                # flush widget section

                self._queue.flush(

                    "widget",

                    widget=_widget,

                    xml_element=xml_element,

                    # useless genuine data
                    #~ xml_attr=None,
                    #~ xml_attrs=None,
                    #~ addon_attrs=None,
                    #~ attrs=None,
                )

                # ensure values

                _attributes = _attributes.flatten()

                # register object

                self._register_object_by_id(

                    _widget, _attributes.get("id")
                )

                # strip out unwanted

                self.TK_CONFIG = tools.dict_delete_items(

                    self.TK_CONFIG,

                    "variable", "value", "indicatoron",
                )

                # widget configure

                self._set_widget_config(_widget, self.TK_CONFIG)

            # end if

            # set layout

            self._set_layout(_widget, _attributes, tk_parent)

            # group -> children

            if xml_tag == "group":

                # loop on XML element children

                return self._loop_on_children(

                    xml_element, _widget,

                    accept = self.DTD.get(xml_tag),
                )

            # end if

            # succeeded

            return True

        # end if

        # failed

        return False

    # end def



    def _info (self, text=None):
        r"""
            raises info events for an eventually existing
            mainwindow's statusbar object;
        """

        # notification event

        self.events.raise_event("StatusBarInfo", text)

    # end def



    def _notify (self, text=None, delay=None):
        r"""
            raises notification events for an eventually existing
            mainwindow's statusbar object;
        """

        # notification event

        self.events.raise_event("StatusBarNotify", text, delay)

    # end def



    def _open_item (self, *args, **kw):
        r"""
            opening clicked item;
        """

        # acknowledge item opening

        self.events.raise_event(

            "GameSectionBrowserOpenItem", *args, **kw
        )

    # end def



    def _open_section (self, *args, **kw):
        r"""
            opening clicked section;
        """

        # safety inits

        if not self.is_tree(self.get_xml_tree()):

            return

        # end if

        # param inits

        # $ 2014-03-13 RS $
        # CAUTION:
        # do *NOT* change this

        _xml_element = tools.choose(

            kw.get("xml_element"),

            dict(id=None),
        )

        _section_id = tools.choose_str(

            kw.get("section_id"),

            _xml_element.get("id"),
        )

        # 'home' requested?

        if kw.get("home"):

            _xml_element = self.get_xml_tree().getroot()

        elif not self.is_element(_xml_element):

            _xml_element = self.get_element_by_id(_section_id)

        # end if

        if _xml_element and len(_xml_element):

            # member inits

            self._parent_section_id = None

            self._cvar.set("")

            # clear children

            for _w in self.viewport.container.winfo_children():

                _w.pack_forget()

                _w.grid_forget()

                _w.place_forget()

            # end for

            try:

                self._loop_on_children(

                    xml_element = _xml_element,

                    tk_parent = self.viewport.container,

                    accept = self.DTD.get(_xml_element.tag),
                )

                self.viewport.container.update_idletasks()

            except Exception as e:

                MB.showerror(

                    _("Error"),

                    _("An exception has raised:\n{error}")

                    .format(error=str(e)),

                    parent=self,
                )

                exit("Error: " + str(e))

            # end try

            # init parent section

            _parent = self.get_xml_tree().find(

                ".//*[@id='{value}']/.."

                .format(value = _xml_element.get("id"))
            )

            if _parent:

                self._parent_section_id = _parent.get("id")

            # end if

            # update keywords

            kw.update(

                parent_section_id = self._parent_section_id,

                xml_element = _xml_element,
            )

            # acknowledge section opening

            self.events.raise_event(

                "GameSectionBrowserOpenSection", *args, **kw
            )

        # end if

    # end def



    def _parse_attr_main (self, attribute, **kw):
        r"""
            main Python exe script attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_any_value_support(attribute, **kw)  # -----------------FIXME?

    # end def



    def _parse_attr_package (self, attribute, **kw):
        r"""
            item own directory attribute;

            no return value (void);
        """

        # param controls

        if self._is_new(attribute):

            # parsed attribute inits

            attribute.value = tools.choose_str(

                tools.normalize_id(attribute.value),

                "misc",
            )

            attribute.update_xml_element()

            attribute.parsed = True

        # end if

    # end def



    def _parse_attr_src (self, attribute, **kw):
        r"""
            zip archive remote src attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_any_value_support(attribute, **kw)  # -----------------FIXME?

    # end def



    def _parse_attr_type (self, attribute, **kw):
        r"""
            item type attribute;

            no return value (void);
        """

        # parsed attribute inits

        kw.update(

            default = "game",

            values = ("editor", ),
        )

        self._fix_values(attribute, **kw)

    # end def



    def _parse_attr_image (self, attribute, attrs, **kw):
        r"""
            image attribute;

            no return value (void);
        """

        # param controls

        if self._is_unparsed(attribute):

            # inits

            _list = [

                attribute.value,

                OP.join(self.IMAGES_DIR, attribute.value),

                self.IMAGE_UNKNOWN,
            ]

            for _path in _list:

                _path = P.normalize(_path)

                if OP.isfile(_path):

                    break

                # end if

            # end for

            # parsed attribute inits

            attribute.value = self.set_image(_path)

            self._tk_config(attribute)

        # end if

    # end def



    def go_home (self, *args, **kw):
        r"""
            shows root section;
        """

        self._open_section(home = True)

    # end def



    def go_parent (self, *args, **kw):
        r"""
            shows parent section;
        """

        if tools.is_pstr(self._parent_section_id):

            self._open_section(section_id = self._parent_section_id)

        else:

            self.go_home()

        # end if

    # end def



    def init_widget (self, **kw):
        r"""
            widget main inits;
        """

        # super class inits

        super().init_widget(**kw)

        # default values

        self.IMAGE_UNKNOWN = P.normalize(

            OP.join(self.IMAGES_DIR, self.IMAGE_UNKNOWN)
        )

        # member inits

        self.slot_owner = self

        self.tk_owner = self.viewport.container

        self._parent_section_id = None

        self._cvar = TK.StringVar()

    # end def



    def web_build (self, filename=None):
        r"""
            tries to build view from remote file before trying locally;
        """

        # not an XML source code?

        if not self.is_xml(filename):

            # already an URL?

            if str(filename).startswith("http"):

                # URL inits

                _url = str(filename)

            else:

                # build URL

                _url = OP.join(

                    self.XML_RC.get("mirror_url"),

                    self.XML_RC.get("dir", "").lstrip("^/"),

                    tools.choose_str(

                        filename,

                        self.XML_RC.get("filename"),

                        "tkgame_sections",
                    )
                    + "."
                    + tools.choose_str(

                        self.XML_RC.get("file_ext"),

                        "xml",

                    ).strip(".")
                )

            # end if - URL

            # notify event

            self._notify(
                _(
                    "Trying to contact mirror web site. "
                    "Please, wait..."
                )
            )

            # get web response to request

            try:

                _response = WEB.urlopen(_url)

            except:

                _response = None

                # notify event

                self._notify(
                    _(
                        "Unable to reach web mirror. "
                        "Trying locally..."
                    )
                )

            # end try

            if _response:

                # notify event

                self._notify(_("Web mirror reached. OK."))

                # get data

                _data = _response.read()

                # look for encoding in data

                _encoding = re.search(

                    r"\bencoding:\s*([\w\-]+)",

                    str(_data)
                )

                if _encoding:

                    _encoding = _encoding.group(0)

                else:

                    _encoding = "UTF-8"

                # end if

                # get clean data as XML script

                filename = _data.decode(_encoding)

            # end if - _response

        # end if - not XML?

        # build GUI

        self.xml_build(filename)

    # end def

# end class GameSectionView
