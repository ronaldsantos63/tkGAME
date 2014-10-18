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

# module private member
__event_manager = None


# app-wide unique instance getter
def get_event_manager ():
    r"""
        app-wide unique instance getter;
    """
    global __event_manager
    if not isinstance(__event_manager, TkGameEventManager):
        __event_manager = TkGameEventManager()
    # end if
    return __event_manager
# end def


class TkGameEventManager:
    """
        simplified signal/slot universal event manager;
    """

    def __init__ (self):
        """
            class constructor
        """
        # member inits
        self.connections = dict()
    # end def


    def connect (self, signal, *slots):
        """
            connects signal name to multiple callback slots;
            returns True on success, False otherwise;
        """
        # get signal current set of slots
        _slots = self.connections.setdefault(signal, set())
        # signal do have a set of slots
        if isinstance(_slots, set):
            # slots must be unique for each signal
            _slots.update(set(slots))
            # update signal set of slots
            self.connections[signal] = set(filter(callable, _slots))
            # operation succeeded
            return True
        # end if
        # operation failed
        return False
    # end def


    def connect_dict (self, events_dict):
        """
            connects (signal, slots) pairs in dict() object;
            slots can be a single callback or one of tuple, list, set;
            returns True on success, False otherwise;
        """
        # param controls
        if events_dict and isinstance(events_dict, dict):
            # loop on items
            for (_signal, _slots) in events_dict.items():
                if isinstance(_slots, (tuple, list, set)):
                    self.connect(_signal, *_slots)
                else:
                    self.connect(_signal, _slots)
                # end if
            # end for
            # operation succeeded
            return True
        # unsupported
        else:
            raise TypeError("Expected plain dict() object type.")
        # end if
        # operation failed
        return False
    # end def


    def disconnect (self, signal, *slots):
        """
            disconnects list of callback slots from signal name;
            returns True if signal exists, False otherwise;
        """
        # get signal current set of slots
        _slots = self.connections.get(signal)
        # signal does exist and has a set of slots
        if _slots and isinstance(_slots, set):
            # remove eventual existing slots
            _slots.difference_update(set(slots))
            # update signal set of slots
            self.connections[signal] = set(filter(callable, _slots))
            # operation succeeded
            return True
        # end if
        # operation failed - unknown signal name
        return False
    # end def


    def disconnect_all (self, *signals):
        """
            disconnects all callback slots from each signal listed;
            if signals list is omitted, disconnects really all
            registered signals;
        """
        # asked for all clear?
        if not signals:
            self.connections.clear()
        # listed clean-up
        else:
            # browse signals list
            for _signal in set(signals):
                # signal is no longer useful
                self.connections.pop(_signal, None)
            # end for
        # end if
    # end def


    def disconnect_dict (self, events_dict):
        """
            disconnects (signal, slots) pairs in dict() object;
            slots can be a single callback or one of tuple, list, set;
            returns True on success, False otherwise;
        """
        # param controls
        if events_dict and isinstance(events_dict, dict):
            # loop on items
            for (_signal, _slots) in events_dict.items():
                if isinstance(_slots, (tuple, list, set)):
                    self.disconnect(_signal, *_slots)
                else:
                    self.disconnect(_signal, _slots)
                # end if
            # end for
            # operation succeeded
            return True
        # unsupported
        else:
            raise TypeError("Expected plain dict() object type.")
        # end if
        # operation failed
        return False
    # end def


    def disconnect_group (self, groupname):
        """
            disconnects only signals which name starts with @groupname;
            for each signal, all slots are removed at once;
        """
        # browse signals list
        for _signal in set(self.connections):
            # signal in group?
            if str(_signal).startswith(groupname):
                # disconnect signal
                self.connections.pop(_signal, None)
            # end if
        # end for
    # end def


    def raise_event (self, signal, *args, **kw):
        """
            calls all attached slots to the given signal name  with
            eventual arguments and keywords;
            returns True if signal exists, False otherwise;
        """
        # get signal current set of slots
        _slots = self.connections.get(signal)
        # signal do exist and has a set of slots
        if _slots and isinstance(_slots, set):
            # keep only callable slots
            _slots = set(filter(callable, _slots))
            # update signal slots collection
            self.connections[signal] = _slots
            # browse the set
            for _slot in _slots.copy():
                # call each slot one by one
                # with arguments and keywords
                _slot(*args, **kw)
            # end for
            # operation succeeded
            return True
        # end if
        # operation failed - unknown signal name
        return False
    # end def

# end class TkGameEventManager
