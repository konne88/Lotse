#!/usr/bin/env python
#coding=utf-8
#
#       status_box.py
#       
#       Copyright 2009 Niklas Schnelle <niklas@niklas-iMac>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.




import gtk
import gobject

from session.waypoint import Waypoint
from session.coordinates import Coordinates
from session import Session
from radar import Radar

class StatusBox(gtk.HBox):
    def __init__(self,session):
        super(StatusBox,self).__init__()
        self._session = session
        
        self._progress = gtk.ProgressBar()
        self.pack_start(self._progress,False, False)
        
        self._info = gtk.Label()
        self._info.set_alignment(xalign=0.01,yalign=0.5)
        self.pack_start(self._info)

        self._session.position_changed += self.on_position_changed

    def on_position_changed(self):
        spos = self._session.sleek_position
        self._progress.set_fraction(spos.judge_quality())
        
        if spos.fix == 2: s = '2D Fix'
        elif spos.fix == 3: s = '3D Fix'
        else: s= 'No Fix'
        
        s+= ', Satellites used: %.0f'%spos.satellites_used
        
        self._info.set_text(s)

        
