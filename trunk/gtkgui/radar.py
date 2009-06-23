#!/usr/bin/env python

import pygtk
import gobject
import pango
import gtk
import math
import time
from gtk import gdk
import cairo

from session.coordinates import Coordinates
from session.waypoint import Waypoint
from session.position import Position

from session.coordinates import Coordinates
from session.waypoint import Waypoint
from session.position import Position

ARROW_HEIGHT = 13
ARROW_WIDTH = 20
ARROW_RADAR_DISTANCE = 4
ARROW_BORDER_DISTANCE = 3

RADAR_REQUEST_SIZE = 300
POINT_RADIUS = 3
RADAR_RADIUS_IN_KM=1
CENTER_POINT_RADIUS = 2

CROSSHAIR_LINE_WIDTH = 1
NORTH_COLOR = (1,0,0)
HEADING_COLOR = (0,0,0)

class Radar(gtk.Widget):
    __gsignals__ = { 'realize': 'override',
                     'expose-event' : 'override',
                     'size-allocate': 'override',
                     'size-request': 'override',}

    def __init__(self,position, target, wpList):
        super(Radar,self).__init__()
        self._position = position
        self._target = target
        self._wpList = wpList
    
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
        requisition.width = RADAR_REQUEST_SIZE
        requisition.height = RADAR_REQUEST_SIZE

    def do_size_allocate(self, allocation):
        self.allocation = allocation
        if self.flags() & gtk.REALIZED:
            self.window.move_resize(*allocation)
    
    def draw_arrow(self,cr,radius,arc,color):
        if a_arc==a_arc:
            cr.rotate(arc)

            cr.set_source_rgb(color[0], color[1], color[2])
            cr.move_to(-ARROW_WIDTH/2,-(radius+ARROW_RADAR_DISTANCE))
            cr.rel_line_to (ARROW_WIDTH, 0)
            cr.rel_line_to (-ARROW_WIDTH/2, -ARROW_HEIGHT)
            cr.close_path()
            cr.stroke()
            
            cr.rotate(-arc)
    
    def draw_coordinate_point(self,cr,radius,coord,maxDist,color):
        #distance to point from centre in drawing coordinates
        drawing_distance = self.position.distance_to(coord)*(radius/maxDist)
        if drawing_distance <= radius:
            alpha = math.radians(self.position.relative_heading_to(coord))
            x = math.sin(alpha)*drawing_distance
            y = -math.cos(alpha)*drawing_distance
            
            cr.set_source_rgb(color[0],color[1],color[2])
            cr.arc(x, y, POINT_RADIUS , 0, 2 * math.pi)
            cr.fill()
            return True
            
        return False

    def do_expose_event(self, event):
        cr = self.window.cairo_create()

        x, y, w, h = self.allocation
        radius = min(w,h)/2 - (ARROW_BORDER_DISTANCE+
                               ARROW_HEIGHT+
                               ARROW_RADAR_DISTANCE)
        cr.translate(w/2,h/2)
        
        # background
        cr.arc(0, 0, radius , 0, 2 * math.pi) 
        cr.set_source_rgb(1, 1, 1)
        cr.fill_preserve()
        cr.set_source_rgb(0, 0, 0)
        cr.stroke()
        # crosshair
        cr.set_line_width(1)
        cr.set_source_rgb(0.7, 0.7, 0.7)
        cr.move_to(-radius,0)
        cr.line_to(radius,0)
        cr.move_to(0,-radius)
        cr.line_to(0,radius)
        cr.stroke()

                      
        m = self._wpList        
        i = m.get_iter_first()
        while i is not None:
            ic = m.iter_children(i)            
            while ic is not None:
                if m.get_value(ic,0) == self.target:
                    self.draw_coordinate_point(cr,radius,self.target,RADAR_RADIUS_IN_KM,HEADING_COLOR)
                    a_arc = math.radians(self.position.relative_heading_to(self.target))            
                    self.draw_arrow(cr,radius,a_arc,HEADING_COLOR);
                else:
                    self.draw_coordinate_point(cr,radius,m.get_value(ic,0),RADAR_RADIUS_IN_KM,(0.5,0.5,0.5))
                ic = m.iter_next(ic)              
            i = m.iter_next(i);
        
        # north arrow
        a_arc = math.radians(-self.position.heading) 
        self.draw_arrow(cr,radius,a_arc,NORTH_COLOR)
                
        # point in the middle
        cr.set_source_rgb(1, 0, 0)
        cr.arc(0, 0, CENTER_POINT_RADIUS , 0, 2 * math.pi) 
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
