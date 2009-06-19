#!/usr/bin/env python

import pygtk
import gobject
import pango
import gtk
import math
import time
from gtk import gdk
import cairo

class Radar(gtk.Widget):
    __gsignals__ = { 'realize': 'override',
                     'expose-event' : 'override',
                     'size-allocate': 'override',
                     'size-request': 'override',}

    def __init__(self,position,target):
        super(Radar,self).__init__()
        self._position = position
        self._target = target
    
    def _redraw(self):
        x, y, w, h = self.allocation
        if self.window is not None:
            self.window.invalidate_rect((0,0,w,h),False)
        
    def do_realize(self):
        self.set_flags(self.flags() | gtk.REALIZED)
        self.window = gdk.Window(self.get_parent_window(),
                                 width=self.allocation.width,
                                 height=self.allocation.height,
                                 window_type=gdk.WINDOW_CHILD,
                                 wclass=gdk.INPUT_OUTPUT,
                                 event_mask=self.get_events() | gdk.EXPOSURE_MASK)
        
        self.window.set_user_data(self)
        self.style.attach(self.window)
        self.style.set_background(self.window, gtk.STATE_NORMAL)
        self.window.move_resize(*self.allocation)

    def do_size_request(self, requisition):
        requisition.width = 300
        requisition.height = 300

    def do_size_allocate(self, allocation):
        self.allocation = allocation
        if self.flags() & gtk.REALIZED:
            self.window.move_resize(*allocation)

    def do_expose_event(self, event):
        cr = self.window.cairo_create()

        x, y, w, h = self.allocation
        a_h = 15
        a_w = 20
        bg_radius = min(w,h)/2 - a_h-5
        cr.translate(w/2,h/2)
        
        # background
        cr.arc(0, 0, bg_radius , 0, 2 * math.pi) 
        cr.set_source_rgb(1, 1, 1)
        cr.fill_preserve()
        cr.set_source_rgb(0, 0, 0)
        cr.stroke()

        # target arrow
        if self.target is not None:
            a_arc = math.radians(self.sleek_position.heading_to(self.target) -
                                 self.sleek_position.heading)
            
            cr.rotate(a_arc)

            cr.set_source_rgb(0, 0, 0)
            cr.move_to(-a_w/2,-bg_radius-2)
            cr.rel_line_to (a_w, 0)
            cr.rel_line_to (-a_w/2, -a_h)
            cr.close_path()
            cr.stroke()
            
            cr.rotate(-a_arc)
    
        cr.set_source_rgb(1, 0, 0)
        cr.move_to(-a_w/2,-bg_radius-2)
        cr.rel_line_to (a_w, 0)
        cr.rel_line_to (-a_w/2, -a_h)
        cr.close_path()
        cr.stroke()
            
        """
        
        a_arc = math.radians(self.position.heading_to(self.target))
        #names are with heading facing up (North)
        a_arcninety = math.radians(90.0)
        
        cr.set_source_rgb(1, 0.3, 0.2)
        cr.move_to(-a_w/2)
        
        
        tar_x=math.sin(a_arc)*(min(w,h)/2-a_h-2)
        tar_y=-math.cos(a_arc)*(min(w,h)/2-a_h-2)
        cr.arc(tar_x, tar_y, 4 , 0, 2 * math.pi) 
        cr.fill()            
        """
        cr.set_source_rgb(0, 0, 1)
        cr.move_to(0,0)

        cr.move_to(-a_w/2,a_h/2) # edge left down
        cr.line_to(0,-a_h)
        cr.line_to(a_w/2,a_h/2)

        cr.close_path()
        cr.stroke()
        
        # point in the middle
        cr.set_source_rgb(1, 0, 0)
        cr.arc(0, 0, 2 , 0, 2 * math.pi) 
        cr.fill()

    def get_target(self):
        return self._target
        
    def set_target(self, value):
        self._redraw()
        self._target = value
        
    target = property(get_target,set_target)

    def get_position(self):
        return self._position

    def set_position(self, value):
        self._redraw()
        self._position = value
        
    position = property(get_position,set_position)
