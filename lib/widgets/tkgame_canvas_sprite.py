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
import os.path as OP

# mandatory dependencies
from . import tkgame_events as EM
from . import tkgame_images as IM
from . import tkgame_animations as AP


class TkGameCanvasSprite:
    """
        A sprite is an animated graphical object that manages
        several states such as wait, walk, run, jump, etc;
    """

    # class constants
    IMAGES_DIR = "images/sprites"
    EVENTS_GROUP = "Game"

    STATUS = {
        "default": {
            "loop": False,
            "sequence": False,
            "delay": 0,
        },
    }


    def __init__ (self, owner, canvas, subclassed=False, **kw):
        """
            class constructor;
        """
        # member inits
        self.owner = owner
        self.canvas = canvas
        self.events = EM.get_event_manager()
        self.animations = AP.get_animation_pool()
        self.image_manager = IM.get_image_manager()
        self.images_dir = (
            kw.get("images_dir") or
            OP.join(self.IMAGES_DIR, self.sprite_name)
        )
        self.role = kw.get("role") or ""
        self.locked = False
        self.started = False
        self.__state = None
        self.state = kw.get("state") or "default"
        self.canvas_id = kw.get("cid") or 0
        self.canvas_tags = kw.get("tags") or ""
        self.xy = (kw.get("x"), kw.get("y"))
        # for best simplification - hook method
        if not subclassed:
            self.init_sprite(**kw)
        # end if
    # end def


    def bbox (self):
        """
            returns sprite's bounding box in canvas;
        """
        return self.canvas.bbox(self.canvas_id)
    # end def


    def bind_events (self, *args, **kw):
        """
            hook method to be reimplemented in subclass;
            class event bindings;
        """
        pass
    # end def


    def center_xy (self):
        """
            returns (x, y) center point of sprite in canvas;
        """
        x0, y0, x1, y1 = self.bbox()
        return ((x0 + x1)/2, (y0 + y1)/2)
    # end def


    @property
    def class_name (self):
        """
            READ-ONLY property;
            returns instance's class name;
        """
        return self.__class__.__name__
    # end def


    def destroy (self, *args, **kw):
        """
            event handler for sprite destruction;
            should be reimplemented in subclass;
        """
        # sprite is enabled?
        if not self.locked:
            # lock sprite to avoid unexpected events
            self.locked = True
            # stop animations and free callback references
            self.animations.release(self.image_animation_loop)
            # hook method for more things to do
            self.on_destroy(*args, **kw)
            # remove events before dying!
            self.unbind_events()
            # delete from canvas
            self.canvas.delete(self.canvas_id)
            # notify system (e.g. for garbage collection)
            self.notify_event("Destroyed")
        # end if
    # end def


    def get_event_name (self, action, group=None):
        """
            hook method to be reimplemented in subclass;
            returns current 'event name' along @action for this
            sprite class;
            all arguments are CASE SENSITIVE;
            template: '{event_group}:{sprite_name}:{action}';
            example: Game:Player:Moved;
        """
        # param inits
        group = group or self.EVENTS_GROUP
        # get canonized event name
        return "{}:{}:{}".format(group, self.sprite_name, action)
    # end def


    def get_sprites_from_ids (self, list_ids, exclude=None):
        """
            retrieves registered sprites in owner's dict along with
            @list_ids parameter, excluding @exclude, if any;
            returns sprites list, as ordered as possible;
            this should be reimplemented in subclasses;
        """
        # retrieve sprites list from owner
        return self.owner.get_sprites_from_ids(list_ids, exclude)
    # end def


    def image_animation_loop (self):
        """
            sprite's image animation loop;
        """
        # safety controls
        if self.locked:
            return
        # end if
        # inits
        _status = self.STATUS[self.state]
        _image = self.image_manager.get_image_by_name(
            self.images_dir,
            "{}_{}".format(self.state, self.state_counter)
        )
        if _image:
            # update image
            self.canvas.itemconfigure(self.canvas_id, image=_image)
            if _status.get("sequence"):
                # next step
                self.state_counter += 1
                # next loop
                self.animations.run_after(
                    _status.get("delay") or 100,
                    self.image_animation_loop
                )
            # end if
        elif self.state_counter:
            if _status.get("loop"):
                # reset counter
                self.state_counter = 0
                # retry once
                self.image_animation_loop()
            else:
                # sequence ended
                self.on_sequence_end()
            # end if
        # end if
    # end def


    @property
    def images_dir (self):
        """
            sprite's images directory;
        """
        return self.__images_dir
    # end def

    @images_dir.setter
    def images_dir (self, value):
        self.__images_dir = OP.abspath(OP.expanduser(value))
    # end def

    @images_dir.deleter
    def images_dir(self):
        del self.__images_dir
    # end def


    def init_sprite (self, **kw):
        """
            hook method to be reimplemented in subclass;
            this avoids re-declaring __init__ signatures all the time;
        """
        # put your own code in subclasses
        pass
    # end def


    def load_images (self):
        """
            cacheing all sprite states pictures;
        """
        self.image_manager.load_images(self.images_dir)
    # end def


    def look_ahead (self, dx, dy):
        """
            looks around current sprite to see who might collide;
            this could be reimplemented in subclasses;
        """
        # inits
        x, y = self.center_xy()
        dxy = (x + dx, y + dy)
        # retrieve sprites list
        sprites = self.get_sprites_from_ids(
            # look ahead
            self.canvas.find_overlapping(*(dxy * 2)),
            # exclude list of ids
            exclude=(self.canvas_id,)
        )
        # return data
        return {"sprites": sprites, "dx": dx, "dy": dy, "dxy": dxy}
    # end def


    def move_animation (self, c_dict):
        """
            here is the animation of a moving sprite;
        """
        # safety controls
        if self.locked:
            return
        # end if
        # moving is quite simple here
        # but you can reimplement this in your own subclasses
        dx, dy = c_dict["dx"], c_dict["dy"]
        # relative move on canvas
        self.canvas.move(self.canvas_id, dx, dy)
        # update pos
        self.x += dx
        self.y += dy
        # notify system
        self.notify_event("Moved")
    # end def


    def move_sprite (self, sx, sy, callback=None):
        """
            moves sprite along callback function's truth return
            value; if callback is omitted, sprite will move when no
            other sprite is encountered at destination place;
            callback function will get in argument
            self.look_ahead()'s return value;
        """
        # safety controls
        if self.locked:
            return
        # end if
        # param inits
        if not callable(callback):
            callback = lambda c_dict: not c_dict.get("sprites")
        # end if
        # look ahead
        c_dict = self.look_ahead(sx, sy)
        # allowed to move?
        if callback(c_dict):
            # notify system
            self.notify_event("Moving")
            # move sprite
            self.move_animation(c_dict)
            # confirm sprite has moved
            return True
        # end if
        # no moves
        return False
    # end def


    def notify_event (self, action):
        """
            hook method to be reimplemented in subclass;
            notifies application of some general and specific actions;
        """
        # general notification
        self.events.raise_event(
            "Canvas:Sprite:{}".format(action), sprite=self
        )
        # specific notification
        self.events.raise_event(
            self.get_event_name(action), sprite=self
        )
    # end def


    def on_destroy (self, *args, **kw):
        """
            this is called at self.destroy(), just after animation
            lockouts and before self.unbind_events(); hook method to be
            reimplemented in subclass;
        """
        pass
    # end def


    def on_sequence_end (self, *args, **kw):
        """
            this is called once a status image sequence ends; hook
            method to be reimplemented in subclass;
        """
        pass
    # end def


    def on_start (self, *args, **kw):
        """
            hook method to be reimplemented in subclass; this is called
            at self.start(), just after self.setup() and before
            self.bind_events();
        """
        # enter the loop
        self.update_image_animation_loop()
    # end def


    def setup (self):
        """
            sets up sprite on canvas, if not already done;
            this is called at most once at self.start();
        """
        # sets up sprite if not already done
        if not self.canvas_id:
            # create sprite on canvas
            self.canvas_id = self.canvas.create_image(
                self.x, self.y,
                anchor="center",
                tags=self.canvas_tags,
            )
            # load sprite's animation pictures
            self.load_images()
            # notify sprite's creation (e.g. for registration)
            self.notify_event("Setup")
        # end if
    # end def


    @property
    def sprite_name (self):
        """
            READ-ONLY property;
            hook method to be reimplemented in subclass;
            returns sprite's genuine name (case-sensitive);
            you may define some logic along with your own sprite
            naming convention;
        """
        return "Sprite"
    # end def


    def start (self):
        """
            starting sprite's image animation loop; will call
            respectively self.setup(), self.on_start() and finally
            self.bind_events();
        """
        # not already running?
        if not self.started:
            # sprite is now started
            self.started = True
            # set up sprite if not already done
            self.setup()
            # hook method for subclass
            self.on_start()
            # bind events
            self.bind_events()
            # notify system
            self.notify_event("Started")
        # notify error
        else:
            raise TkGameSpriteError("sprite has already been started.")
        # end if
    # end def


    @property
    def state (self):
        """
            sprite's current state;
        """
        return self.__state
    # end def

    @state.setter
    def state (self, value):
        # param controls
        if value in self.STATUS:
            # state has changed?
            if self.__state != value:
                # reset counter
                self.state_counter = 0
            # end if
            # new state inits
            self.__state = value
            # update animation loop if started
            self.update_image_animation_loop()
            # notify system
            self.notify_event("State:Changed")
        else:
            raise TkGameSpriteError(
                "unsupported value '{v}' for 'state' attribute."
                .format(v=value)
            )
        # end if
    # end def

    @state.deleter
    def state (self):
        del self.__state
    # end def


    def stop (self):
        """
            stops image animation loop;
        """
        # inits
        self.started = False
        self.animations.stop(self.image_animation_loop)
    # end def


    def unbind_events (self, *args, **kw):
        """
            hook method to be reimplemented in subclass;
            class event unbindings;
        """
        pass
    # end def


    def update_image_animation_loop (self):
        """
            updates sprite's image animation loop;
        """
        # allowed to proceed?
        if self.started and not self.locked:
            # threaded animation loop
            self.animations.run_after(1, self.image_animation_loop)
        # end if
    # end def


    @property
    def x (self):
        """
            x coordinate of current sprite;
        """
        return self.__x
    # end def

    @x.setter
    def x (self, value):
        self.__x = value or 0
    # end def

    @x.deleter
    def x (self):
        del self.__x
    # end def


    @property
    def xy (self):
        """
            (x, y) coordinates of current sprite;
        """
        return (self.x, self.y)
    # end def

    @xy.setter
    def xy (self, tuple_xy):
        self.x, self.y = tuple_xy
    # end def

    @xy.deleter
    def xy (self):
        del self.x, self.y
    # end def


    @property
    def y (self):
        """
            y coordinate of current sprite;
        """
        return self.__y
    # end def

    @y.setter
    def y (self, value):
        self.__y = value or 0
    # end def

    @y.deleter
    def y (self):
        del self.__y
    # end def

# end class TkGameCanvasSprite


# error handling

class TkGameSpriteError (Exception):
    """
        handles sprite specific errors;
    """
    pass
# end class TkGameSpriteError
