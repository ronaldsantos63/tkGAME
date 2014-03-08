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

import tkRAD

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

        self.navbar.pack(expand=0, fill=TK.X)

        self.view.pack(expand=1, fill=TK.BOTH)

        # connect events

        self.events.connect_dict(
            {
                "GameSectionNavBarGoHome": None,

                "GameSectionNavBarGoParent": None,
            }
        )

    # def end

# end class



class GameSectionNavBar (tkRAD.RADXMLFrame):
    r"""
        tkGAME game section browser subcomponent (navigation bar);
    """

    def init_widget (self, **kw):
        r"""
            widget inits;
        """

        # inits

        xml = """
            <tkwidget>
                <style
                    id="navbar"
                    compound="left"
                    relief="flat"
                />
                <button
                    name="btn_home"
                    text="Home"
                    image="^/images/browser/home.gif"
                    command="@GameSectionNavBarGoHome"
                    style="navbar"
                    layout="pack"
                    layout_options="side='left'"
                />
                <button
                    name="btn_go_parent"
                    text="Go to parent"
                    image="^/images/browser/go_parent.gif"
                    command="@GameSectionNavBarGoParent"
                    style="navbar"
                    layout="pack"
                    layout_options="side='left'"
                />
            </tkwidget>
        """

        # build GUI

        self.xml_build(xml)

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

        "dir": "^/xml/data",

        "filename": "tkgame_sections",

        "file_ext": ".xml",

    } # end of XML_RC



    def __init__ (self, master = None, **kw):

        # default values

        self.CONFIG = self.CONFIG.copy()

        self.CONFIG.update(kw)

        # super inits

        TK.ttk.Frame.__init__(self, master)

        self.configure(**self._only_tk(self.CONFIG))

        self.tk_parent = master

        RADXMLWidget.__init__(self, tk_owner = self, **self.CONFIG)

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

                xml_element, tk_parent, accept=self.DTD.get(xml_tag),
            )

        # end if

        # failure

        return False

    # end def



    def _build_view_item (self, xml_tag, xml_element, tk_parent):
        r"""
            protected method def;

            builds any tkinter native widget along its class name;

            returns True on build success, False otherwise;
        """

        # param controls

        if self.cast_element(xml_element):

            # set real classname

            xml_element.set("class", "Button")

            # must force XML attr module name

            xml_element.set("module", "ttk.")

            # build widget

            return self._build_element_widget(

                xml_tag,  xml_element,  tk_parent,
            )

        # end if

        # failed

        return False

    # end def


# end class GameSectionView
