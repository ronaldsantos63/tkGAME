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
from . import tkgame_events as EM
from . import tkgame_images as IM
from . import tkgame_animations as AP


class TkGameSprite:
    """
        A sprite is an animated graphical object that manages
        several states such as wait, walk, run, jump, etc;
    """

    # class constants
    STATUS = {
        "default": {
            "loop": False,
            "sequence": False,
            "delay": 0,
        },
    }

    CELLSIZE = 64


    def __init__ (self, owner, canvas, **kw):
        """
            class constructor
        """
        # member inits
        self.owner = owner
        self.canvas = canvas
        self.events = EM.get_event_manager()
        self.animations = AP.get_animation_pool()
        self.image_manager = IM.get_image_manager()
        self.images_dir = kw.get("images_dir") or ""
        self.state = kw.get("state") or "default"
        self.canvas_id = kw.get("cid") or 0
        self.canvas_tags = kw.get("tags") or ""
        self.cellsize = kw.get("cellsize") or self.CELLSIZE
        self.dict_ids = kw.get("dict_ids") or dict()
        self.x = kw.get("x") or 0
        self.y = kw.get("y") or 0
    # end def


    def bbox (self):
        """
            returns sprite's bounding box in canvas
        """
        return self.canvas.bbox(self.canvas_id)
    # end def


    def center_xy (self):
        """
            returns (x, y) center point of sprite in canvas
        """
        x0, y0, x1, y1 = self.bbox()
        return ((x0 + x1)/2, (y0 + y1)/2)
    # end def


    def collisions (self, xy=None):
        """
            returns list of canvas IDs of sprites colliding with
            this current sprite; this list excludes current sprite's
            ID; parameter xy must be an (x, y) tuple i.e. xy=(x, y);
        """
        # param inits
        if xy is None:
            # sprite inbound collision detection
            xy = self.bbox()
        else:
            # sprite outbound collision detection
            xy *= 2
        # end if
        # get collisions
        collisions = list(self.canvas.find_overlapping(*xy))
        # strip out self id
        if self.canvas_id in collisions:
            collisions.remove(self.canvas_id)
        # end if
        return collisions
    # end def


    def look_ahead (self, sx, sy):
        """
            looks around current sprite to see who might collide;
        """
        # inits
        dx = sx * self.cellsize
        dy = sy * self.cellsize
        sprite = None
        # look ahead
        collisions = self.collisions(xy=(self.x + dx, self.y + dy))
        if collisions:
            sprite = self.dict_ids.get(collisions[0])
        # end if
        return {"sprite": sprite, "dx": dx, "dy": dy}
    # end def


    def move_sprite (self, sx, sy, callback=None):
        """
            moves sprite along callback function's truth return
            value; if callback is omitted, sprite will move when no
            other sprite is encountered at destination place;
            callback function will get in argument
            self.look_ahead()'s return value;
        """
        # param inits
        if not callable(callback):
            callback = lambda c: not c["sprite"]
        # end if
        # look ahead
        c_dict = self.look_ahead(sx, sy)
        # allowed to move?
        if callback(c_dict):
            # move sprite
            self.move_animation(c_dict)
        # end if
    # end def


    def move_animation (self, c_dict):
        """
            here is the animation of a moving sprite
        """
        # moving is quite simple here
        # but you can reimplement this in your own subclasses
        self.canvas.move(self.canvas_id, c_dict["dx"], c_dict["dy"])
        # update pos
        self.x += c_dict["dx"]
        self.y += c_dict["dy"]
    # end def


    def start (self):
        """
            starting sprite's image animation loop; sprite's owner
            must implement an owner.register_sprite(canvas_id,
            sprite) method;
        """
        # sets up sprite if not already done
        if not self.canvas_id:
            self.canvas_id = self.canvas.create_image(
                self.x, self.y, anchor='center', tags=self.canvas_tags,
            )
            # notify sprite creation (e.g. for registering)
            self.events.raise_event(
                "Canvas:Sprite:Created",
                canvas_id=self.canvas_id,
                sprite=self,
            )
            # loading sprite's animation pictures
            self.load_images()
        # end if
        # enter the loop
        self.animations.run_after(1, self.image_animation_loop)
    # end def


    def image_animation_loop (self):
        """
            sprite's image animation loop
        """
        # inits
        _status = self.STATUS[self.state]
        _image = self.image_manager.get_image(
            OP.abspath(
                OP.join(
                    self.images_dir,
                    "{}_{}.gif".format(self.state, self.state_counter)
                )
            )
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


    def on_sequence_end (self, *args, **kw):
        """
            this is called once a status image sequence ends;
            please, feel free to override this in your own subclasses;
        """
        pass
    # end def


    def load_images (self):
        """
            cacheing all sprite states pictures
        """
        self.image_manager.load_images(self.images_dir)
    # end def


    @property
    def images_dir (self):
        """
            sprite's images directory
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


    @property
    def state (self):
        """
            sprite's current state
        """
        return self.__state
    # end def

    @state.setter
    def state (self, value):
        self.__state = str(value)
        self.state_counter = 0
    # end def

    @state.deleter
    def state (self):
        del self.__state
    # end def


    @property
    def xy (self):
        """
            (x, y) coordinates of current sprite
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

# end class TkGameSprite
