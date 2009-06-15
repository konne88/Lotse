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
        if True:#self.target is not None:
            a_arc = 2#math.radians(self.position.heading_to(self.target))
            cr.rotate(a_arc)

            cr.set_source_rgb(0, 0, 0)
            cr.move_to(-a_w/2,-bg_radius-2)
            cr.rel_line_to (a_w, 0)
            cr.rel_line_to (-a_w/2, -a_h)
            cr.close_path()
            cr.stroke()
            
            cr.rotate(-a_arc)
        
            cr.rotate(3)
            
            cr.set_source_rgb(0, 0, 0)
            cr.move_to(-a_w/2,-bg_radius-2)
            cr.text_path ("N");
            
            cr.rotate(-3)
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
            
        #  heading arrow
        #if self.position.heading<=360.0 and self.position.heading>=0:
        a_arc = math.radians(45.0)#self.position.heading)
        #names are with heading facing up (North)
        a_arcninety = math.radians(150.0)
        
        cr.set_source_rgb(0, 0, 1)
        cr.move_to(0,0)
        x_leftdown=math.sin(a_arc-a_arcninety)*(a_w/2)
        y_leftdown= -math.cos(a_arc-a_arcninety)*(a_w/2)
        
        x_rightdown = math.sin(a_arc+a_arcninety)*(a_w/2)
        y_rightdown = -math.cos(a_arc+a_arcninety)*(a_w/2)
        
        x_tip=math.sin(a_arc)*a_h
        y_tip=-math.cos(a_arc)*a_h
        cr.move_to(x_leftdown,y_leftdown) # edge left down
        cr.line_to(x_tip,y_tip)
        cr.line_to(x_rightdown,y_rightdown)

        cr.close_path()
        cr.stroke()
            
              

        # point in the middle
        cr.set_source_rgb(1, 0, 0)
        cr.arc(0, 0, 2 , 0, 2 * math.pi) 
        cr.fill()

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        self._redraw()
        self._target = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._redraw()
        self._position = value
