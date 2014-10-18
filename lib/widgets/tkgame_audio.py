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


# debugging mode
DEBUG = False
#~ DEBUG = True


# module private member
__player_class = object


def tron (message, *args, **kw):
    """
        traces on messages for debugging session (TRON);
    """
    if DEBUG:
        print("tkGAME::audio: {}".format(message), *args, **kw)
    # end if
# end def


def new_audio_player (*args, **kw):
    """
        looks for available audio player;
        returns new instance of audio player if supported;
        returns SilentAudioPlayer instance otherwise;
    """
    global __player_class
    # got to look out?
    if not issubclass(__player_class, BaseAudioPlayer):
        # supported audio player types
        supported = (WindowsAudioPlayer, GstAudioPlayer)
        for ptype in supported:
            try:
                ptype(*args, **kw)
                __player_class = ptype
                break
            except:
                # debugging session
                tron("unsupported player type:", ptype.__name__)
                __player_class = None
            # end try
        # end for
        # set default if unsupported
        __player_class = __player_class or SilentAudioPlayer
    # end if
    # debugging session
    tron("instantiating player type:", __player_class.__name__)
    # return new player instance
    return __player_class(*args, **kw)
# end def


class BaseAudioPlayer:
    """
        Generic asynchronous audio player class (interface);
    """

    def __del__ (self):
        """ Class destructor """
        tron("garbage collection (GC) asked for", self)
        self.on_garbage_collection()
        tron("GC suppressed player:", self)
    # end def


    def __init__ (self, volume=None):
        """ Class initialiser """
        tron("initializing:", self)
        self.volume = volume or 1.0
    # end def


    @property
    def classname (self):
        """
            read-only property for instance class name;
        """
        return self.__class__.__name__
    # end def


    def on_garbage_collection (self):
        """
            hook method to be reimplemented in subclass;
        """
        # stop playing
        self.stop()
    # end def


    def pause (self):
        """
            pauses audio data playback;
        """
        # must be implemented in subclasses
        tron(
            "{}.pause(): not implemented yet."
            .format(self.classname)
        )
    # end def


    def play (self, uri, volume=None):
        """
            plays audio data retrieved from @uri at @volume level;
        """
        # must be implemented in subclasses
        tron(
            "{}.play(): not implemented yet."
            .format(self.classname)
        )
    # end def


    def resume (self):
        """
            resumes audio data playback;
        """
        # must be implemented in subclasses
        tron(
            "{}.resume(): not implemented yet."
            .format(self.classname)
        )
    # end def


    def set_volume (self, volume):
        """
            sets volume of audio data playback;
        """
        # must be implemented in subclasses
        tron(
            "{}.set_volume(): not implemented yet."
            .format(self.classname)
        )
    # end def


    def stop (self):
        """
            stops audio data playback;
        """
        # must be implemented in subclasses
        tron(
            "{}.stop(): not implemented yet."
            .format(self.classname)
        )
    # end def

# end class BaseAudioPlayer


class SilentAudioPlayer (BaseAudioPlayer):
    """
        Dummy class for unsupported audio players;
    """

    def __init__ (self, volume=None):
        """ Class initialiser """
        # super class inits
        super().__init__(volume)
        # debugging session
        tron(
            "unsupported audio players - using silent player instead."
        )
    # end def

# end class SilentAudioPlayer


class WindowsAudioPlayer (BaseAudioPlayer):
    """
        MS-Windows(tm) audio playback wrapper class;
    """

    def __init__ (self, volume=None):
        """ Class initialiser """
        global WS
        # super class inits
        super().__init__(volume)
        # winsound support
        import winsound as WS
        self.flags = WS.SND_FILENAME | WS.SND_ASYNC | WS.SND_NODEFAULT
    # end def


    def on_garbage_collection (self):
        """
            hook method to be reimplemented in subclass;
        """
        # keep quiet
        pass
    # end def


    def play (self, uri, volume=None):
        """
            plays audio data retrieved from @uri;
            parameter @volume is *NOT* supported by winsound;
        """
        # param inits
        uri = os.path.abspath(uri)
        # reset player
        self.stop()
        # debugging session
        tron("playing audio data from URI:", uri)
        # sound playback
        WS.PlaySound(uri, self.flags)
    # end def


    def stop (self):
        """
            stops playback for eventual pending audio data;
        """
        # stop playing audio data
        WS.PlaySound(None, 0)
        # debugging session
        tron("stopped audio playback.")
    # end def

# end class WindowsAudioPlayer


class GstAudioPlayer (BaseAudioPlayer):
    """
        GNOME GStreamer audio playback wrapper class;
    """

    def __init__ (self, volume=None):
        """ Class initialiser """
        global GObject, Gst
        # super class inits
        super().__init__(volume)
        # GStreamer support
        import gi
        gi.require_version("Gst", "1.0")
        from gi.repository import GObject, Gst
        GObject.threads_init()
        Gst.init()
        self.player = Gst.ElementFactory.make("playbin")
    # end def


    def play (self, uri, volume=None):
        """
            plays audio data retrieved from @uri with @volume;
            resets player to avoid strange loops;
        """
        # param controls
        if ":" not in uri:
            uri = "file://" + os.path.abspath(uri)
        # end if
        if volume is None:
            volume = self.volume
        # end if
        volume = max(0.0, min(2.0, float(volume)))
        # reset player
        self.stop()
        # debugging session
        tron("playing audio data from URI:", uri)
        # init player
        self.player.set_property("uri", uri)
        self.player.set_property("volume", volume)
        self.player.set_state(Gst.State.PLAYING)
    # end def


    def set_volume (self, volume):
        """
            sets volume of audio data playback;
        """
        # param controls
        self.volume = max(0.0, min(2.0, float(volume)))
        self.player.set_property("volume", self.volume)
    # end def


    def stop (self):
        """
            stops playback for eventual pending audio data;
        """
        # CAUTION:
        # 'uri' property must be reset because of multiple calls
        self.player.set_property("uri", "")
        # stop playing audio data
        self.player.set_state(Gst.State.NULL)
        # debugging session
        tron("stopped audio playback.")
    # end def

# end class GstAudioPlayer
