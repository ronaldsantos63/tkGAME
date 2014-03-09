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

import tkinter as TK

import tkinter.messagebox as MB

import tkRAD

from tkRAD.core import tools

from tkRAD.widgets.rad_frame import RADFrame

from tkRAD.xml.rad_xml_widget import RADXMLWidget



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

        self.after(100, self.view.web_build, filename)

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



class GameSectionView (RADXMLWidget, TK.ttk.Frame):
    r"""
        tkGAME game section browser subcomponent (data view);
    """


    CONFIG = {

        # for subclass widget pre-configuration

    } # end of CONFIG



    # XML tree root element
    # overrides RADXMLBase.DOCTYPE

    DOCTYPE = "tksection"



    # accepted XML child elements for XML container element

    DTD = {

        "item": ("none", ),

        "section": ("section", "item"),

        "tksection": ("section", "item"),

    } # end of DTD



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



    def __init__ (self, master = None, **kw):

        # default values

        self.CONFIG = self.CONFIG.copy()

        self.CONFIG.update(kw)

        # super inits

        TK.ttk.Frame.__init__(self, master)

        self.configure(**self._only_tk(self.CONFIG))

        self.tk_parent = master

        self._parent_section_id = None

        self._cvar = TK.StringVar()

        RADXMLWidget.__init__(self, tk_owner = self, **self.CONFIG)

    # end def



    def _build_element_item (self, xml_tag, xml_element, tk_parent):
        r"""
            building <item> XML element;
        """

        # action inits

        xml_element.attrib.setdefault("command", "._open_item")

        # generic view item

        self._build_view_item(xml_tag, xml_element, tk_parent)

    # end def



    def _build_element_section (self, xml_tag, xml_element, tk_parent):
        r"""
            building <section> XML element;
        """

        # action inits

        xml_element.attrib.setdefault("command", "._open_section")

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

            _attrs = self._init_attributes(

                xml_tag, xml_element, tk_parent
            )

            # widget inits

            _widget = self.get_object_by_id(_attrs.get("id"))

            if not _widget:

                # new widget

                _widget = TK.Radiobutton(

                    tk_parent,

                    relief=TK.FLAT,

                    offrelief=TK.FLAT,

                    indicatoron=0,

                    variable=self._cvar,

                    value=_attrs.get("id"),
                )

                # store data in widget

                _widget.xml_element = xml_element

                # register object

                self._register_object_by_id(_widget, _attrs.get("id"))

                # strip out unwanted

                self.TK_CONFIG = tools.dict_delete_items(

                    self.TK_CONFIG,

                    "variable", "value", "indicatoron",
                )

                # widget configure

                self._set_widget_config(_widget, self.TK_CONFIG)

            # end if

            # set layout

            self._set_layout(_widget, _attrs, tk_parent)

            # succeeded

            return True

        # end if

        # failed

        return False

    # end def



    def _notify (self, text=None, delay=None):
        r"""
            raises notification events for an eventually existing
            mainwindow's statusbar object;
        """

        # notification event

        self.events.raise_event("StatusBarNotify", text, delay)

    # end def



    def _open_item (self, item_id=None, *args, **kw):
        r"""
            opening clicked item;
        """

        # param inits

        _widget = self.get_object_by_id(

            tools.choose_str(

                item_id,

                self._cvar.get(),
            )
        )

        _xml_element = getattr(_widget, "xml_element", None)

        # acknowledge item opening

        self.events.raise_event(

            "{cname}OpenItem"
            .format(cname = self.classname()),

            widget = _widget,

            xml_element = _xml_element,
        )

    # end def



    def _open_section (self, section_id=None, home=False, *args, **kw):
        r"""
            opening clicked section;
        """

        # safety inits

        if not self.is_tree(self.get_xml_tree()):

            return

        # end if

        # param controls

        if home:

            _widget = self

            _xml_element = self.get_xml_tree().getroot()

            self._parent_section_id = None

        else:

            _widget = self.get_object_by_id(

                tools.choose_str(

                    section_id,

                    self._cvar.get(),
                )
            )

            _xml_element = getattr(_widget, "xml_element", None)

        # end if

        if _widget and _xml_element and len(_xml_element):

            # inits

            self._cvar.set("")

            # clear children

            for _w in self.winfo_children():

                _w.pack_forget()
                _w.grid_forget()
                _w.place_forget()

            # end for

            try:

                self._loop_on_children(

                    xml_element = _xml_element,

                    tk_parent = self,

                    accept = self.DTD.get(_xml_element.tag),
                )

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

            else:

                self._parent_section_id = None

            # end if

            # acknowledge section opening

            self.events.raise_event(

                "{cname}OpenSection"
                .format(cname = self.classname()),

                widget = _widget,

                xml_element = _xml_element,

                parent_section_id = self._parent_section_id,
            )

        # end if

    # end def



    def go_home (self, *args, **kw):
        r"""
            shows root section;
        """

        self._open_section(home=True)

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



    def web_build (self, filename=None):
        r"""
            tries to build view from remote file before trying locally;
        """

        # param controls - XML markup parens?

        if "<" not in str(filename):

            import urllib.request as WEB

            import os.path as OP

            import re

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
                    "Trying to contact web mirror site. "
                    "Please, wait..."
                )
            )

            # reset filename

            filename = None

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

        # end if - markup "<"

        # build GUI

        self.xml_build(filename)

    # end def

# end class GameSectionView
