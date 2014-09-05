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


# private module member
__animation_pool = None


# app-wide unique instance getter
def get_animation_pool ():
    """
        retrieves app-wide unique instance of animation pool
    """
    global __animation_pool
    if not isinstance(__animation_pool, TkGameAnimationPool):
        __animation_pool = TkGameAnimationPool()
    # end if
    return __animation_pool
# end def


class TkGameAnimationPool:
    """
        Animation pool for Tkinter GUI environment
    """

    def __init__ (self):
        """
            class constructor
        """
        # thread-ids dictionary inits
        self.tid = dict()
        # tkinter default root object
        self.root = TK._default_root
    # end def


    def run_after (self, delay, callback, *args):
        """
            runs a delayed thread;
            parameter @delay is in milliseconds;
        """
        # param inits
        delay = max(1, int(delay))
        # stop previous running thread, if any
        self.stop(callback)
        # schedule new thread id for further call
        self.tid[callback] = self.root.after(delay, callback, *args)
    # end def


    def stop (self, *callbacks):
        """
            stops scheduled threads, if any;
        """
        # browse list of callbacks
        for _cb in callbacks:
            # stop thread
            self.root.after_cancel(self.tid.get(_cb) or 0)
            # remove thread id
            self.tid.pop(_cb, None)
        # end for
    # end def


    def stop_all (self):
        """
            stops all scheduled threads;
            clears up all thread-ids dictionary;
        """
        # loop on all thread ids
        for _tid in self.tid.values():
            # stop scheduled thread
            self.root.after_cancel(_tid)
        # end for
        # clear all dict
        self.tid.clear()
    # end def

# end class TkGameAnimationPool
