#!/usr/bin/env python
#coding=utf-8

#import osso
import hildon
import  os, time, sys

from gtk import *

from source_tab import SourceTab
from goto_tab import GotoTab
from waypoint_tab import WaypointTab
from session import Session
from waypoint import Waypoint

class LotseWindow(hildon.Window):
    def __init__(self,session):
        super(LotseWindow,self).__init__()
        
        self._notebook = Notebook()
        self.add(self._notebook)
        
        self._gotoTab = GotoTab(session)
        self._notebook.append_page(self._gotoTab, Label('Goto'))
        
        self._sourceTab = SourceTab(session)
        self._notebook.append_page(self._sourceTab, Label('Sources'))
        
        self._waypointTab = WaypointTab(session)
        self._notebook.append_page(self._waypointTab, Label('Waypoints'))

        self.connect('destroy', self.window_destroy)
        self.set_geometry_hints(None,640,480)
        self.show_all()     
    
    def window_destroy(self,widget, data=None):
        main_quit()

# If the program is run directly or passed as an argument to the python
# interpreter then create a HelloWorld instance and show it
if __name__ == "__main__":
    #   osso_c = osso.Context("osso_test_app", "0.0.1", False)
    program  = hildon.Program()
    #  self.window = hildon.Window()
  
    session = Session()
    lotse = LotseWindow(session)
    main()

