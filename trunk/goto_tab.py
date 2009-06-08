#coding=utf-8

import gtk
import gobject
from waypoint import Waypoint
from coordinates import Coordinates
from session import Session

class TargetComboBoxEntry(gtk.ComboBoxEntry):
    def __init__(self,model):
        super(TargetComboBoxEntry, self).__init__(model)

    def do_changed(self, a):
        print "That realy sucks"

class GotoTab(gtk.VBox):
    def __init__(self,session):
        super(GotoTab,self).__init__()
        
        self.target = gtk.ComboBox(session.wpList)

 
        renderer = gtk.CellRendererText()
        self.target.pack_start(renderer) 
        self.target.set_cell_data_func(renderer, self.on_render_name)
        
        renderer = gtk.CellRendererText()
        self.target.pack_start(renderer) 
        self.target.set_cell_data_func(renderer, self.on_render_latlon)
        self.target.connect('changed',self.on_target_select)
        
        self.pack_start(self.target,False)
        
        
        self.output = gtk.Label()
        self._session=session
        gobject.timeout_add(100, self.update_output)
        
        self.add(self.output)
        
    def on_render_name(self, celllayout, cell, model, iter):
        v=model.get_value(iter, 0)
        if v!=None:
            cell.set_property('text', model.get_value(iter, 0).name)
        else:
            cell.set_property('text', "")    
        
    def on_render_latlon(self, celllayout, cell, model, iter):
        v = model.get_value(iter, 0)
        if type(v) == Waypoint:
            cell.set_property('text', v.strlatlon())
        else:
            cell.set_property('text', "")
    
    def on_target_select(self, combobox):   
        print "Do as I wish"     

        
                
    def update_output(self):
        wp = self._session.get_current_waypoint()
        
        s  = 'Lat: %.5f °\n'%wp.lat
        s += 'Lon: %.5f °\n'%wp.lon
        s += 'Alt: %.0f m\n'%wp.alt
        s += 'Speed: %.5f m/s\n'%wp.speed
        s += 'Heading: %.1f °'%wp.heading 
        self.output.set_text(s)
        
        return 1
