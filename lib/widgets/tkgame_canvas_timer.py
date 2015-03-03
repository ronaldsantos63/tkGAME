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



class TkGameCanvasTimer:
    """
        Generic Tkinter Canvas Timer;
    """

    # class constant defs
    # this could be overridden in subclass

    TIMER_DELAY = 1000  # in milliseconds (must be an integer)


    def __init__ (self, canvas, tag_or_id, delay=None):
        """
            class constructor;
        """
        # member inits
        self.canvas = canvas
        self.delay = delay
        self.tag_or_id = tag_or_id
        self.thread_id = 0
        self.time_count = 0
    # end def


    @property
    def delay (self):
        """
            property attribute - timer activity loop delay (in msec);
        """
        return self.__delay
    # end def

    @delay.setter
    def delay (self, value):
        """
            property setter; @value cannot be less than 1 msec;
        """
        # try out
        try:
            self.__delay = max(1, int(value))
        except:
            self.__delay = max(1, int(self.TIMER_DELAY))
        # end try
    # end def

    @delay.deleter
    def delay (self):
        """
            property deleter;
        """
        del self.__delay
    # end def


    def get_time_format (self, time_count):
        """
            returns formatted string for @time_count (expressed in
            seconds by default); this hook method should be
            reimplemented in subclass to meet your own needs;
        """
        # inits
        _tc = int(time_count)
        _sec = _tc % 60
        _min = (_tc // 60) % 60
        _hrs = _tc // 3600
        # get time format
        return "{:02d}:{:02d}:{:02d}".format(_hrs, _min, _sec)
    # end def


    def gui_update (self, *args, **kw):
        """
            event handler: update timer display on canvas;
        """
        # update display
        self.canvas.itemconfigure(
            self.tag_or_id,
            text=self.get_time_format(self.time_count),
        )
    # end def


    def reset (self, *args, **kw):
        """
            event handler: stops and resets timer to zero, including
            GUI updates;
        """
        # stop pending timer
        self.stop()
        # reset to zero
        self.time_count = 0
        # update display
        self.gui_update(*args, **kw)
    # end def


    def restart (self, *args, **kw):
        """
            event handler: resets and restarts timer activity;
        """
        # reset timer
        self.reset(*args, **kw)
        # restart timer
        self.start(*args, **kw)
    # end def


    def start (self, *args, **kw):
        """
            event handler: starts or restarts timer activity;
        """
        # no pending thread?
        if not self.thread_id:
            # restart new thread
            self.thread_id = self.canvas.after(
                self.delay, self.timer_loop
            )
        # end if
    # end def


    def stop (self, *args, **kw):
        """
            event handler: stops timer activity;
        """
        # stop pending thread
        self.canvas.after_cancel(self.thread_id)
        # reset thread id
        self.thread_id = 0
    # end def


    def timer_activity (self, *args, **kw):
        """
            event handler: timer's activity;
            hook method to be reimplemented in subclass;
        """
        # increment time count
        self.time_count += 1
        # update display
        self.gui_update(*args, **kw)
    # end def


    def timer_loop (self, *args, **kw):
        """
            event handler: timer activity loop;
        """
        # call hook method
        self.timer_activity(*args, **kw)
        # schedule next activity (loop)
        self.thread_id = self.canvas.after(self.delay, self.timer_loop)
    # end def

# end class TkGameCanvasTimer



def run_test (*args, **kw):
    """
        quick unit tests;
    """
    import tkinter as TK
    root = TK.Tk()
    canvas = TK.Canvas(root, width=200, height=100)
    canvas.create_text(100, 20, anchor=TK.N, tags="timer")
    canvas.pack()
    timer = TkGameCanvasTimer(canvas, "timer", delay=kw.get("delay"))
    timer.reset()
    opts = dict(side=TK.LEFT, padx=5, pady=5)
    TK.Button(root, text="Start", command=timer.start).pack(**opts)
    TK.Button(root, text="Stop", command=timer.stop).pack(**opts)
    TK.Button(root, text="Reset", command=timer.reset).pack(**opts)
    root.mainloop()
# end def


if __name__ == "__main__":
    # quick test
    run_test()
# end if
