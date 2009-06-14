#coding=utf-8

import gtk
import gobject

from session.waypoint import Waypoint
from session.coordinates import Coordinates
from session import Session
from radar import Radar

class GotoTab(gtk.VBox):
    def __init__(self,session):
        super(GotoTab,self).__init__()
        self._session=session
        
        self.target = gtk.ComboBox(session.wpList)
        renderer = gtk.CellRendererText()
        self.target.pack_start(renderer) 
        self.target.set_cell_data_func(renderer, self.on_render_name)
        renderer = gtk.CellRendererText()
        self.target.pack_start(renderer) 
        self.target.set_cell_data_func(renderer, self.on_render_latlon)
        self.target.connect('changed',self.on_target_select)
        self.pack_start(self.target,False)
        
        gotobox = gtk.HBox()        
        self.pack_start(gotobox)        
        self.radar = Radar(session.position, session.target)
        gotobox.pack_start(self.radar,True,True)
        
        textbox = gtk.VBox()
        gotobox.pack_start(textbox,False,False,10)
        self.output_pos = gtk.Label()
        self.output_target = gtk.Label()
        textbox.pack_start(self.output_pos)
        textbox.pack_start(self.output_target)
        
        self._session.position_changed += self.on_position_changed
        self._session.target_changed += self.on_target_changed
        self._session.position_changed += self.on_target_changed
        
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
        iter=combobox.get_active_iter()
        if iter!=None:
            v=self._session.wpList.get_value(iter, 0) 
            if type(v) == Waypoint:
                self._session.target=v

    def on_position_changed(self):
        pos = self._session.position
        
        self.radar.position = pos
        
        s = 'Your Position\n'
        s += pos.strlatlon()+'\n'
        s += 'Alt: %.0f m\n'%pos.alt
        s += 'Speed: %.5f m/s\n'%pos.speed
        s += 'Heading: %.1f °'%pos.heading 
        self.output_pos.set_text(s)
        
    def on_target_changed(self):
        tar = self._session.target
        
        self.radar.target = tar
        
        s = ""
        
        if tar is not None:
            pos = self._session.position
            
            dist_to_target = pos.distance_to(tar)*1000
            head_to_target = pos.heading_to(tar)
            
            s = 'Target\n'
            s += tar.name+'\n'
            s += tar.strlatlon()+'\n'
            s += 'Distance: %.0f m\n'%dist_to_target 
            s += 'Direction %.1f°\n'%head_to_target
            relative_direction=head_to_target-pos.heading
            s += 'Turn %s by '%('left','right')[relative_direction>0]
            s += '%.1f°\n'%abs(relative_direction)
            
        self.output_target.set_text(s)