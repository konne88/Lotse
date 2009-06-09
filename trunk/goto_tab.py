#coding=utf-8

import gtk
import gobject
from waypoint import Waypoint
from coordinates import Coordinates
from session import Session



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
        
        
        self.output_pos = gtk.Label()
        self.output_target = gtk.Label()
        self._session=session
        gobject.timeout_add(100, self.update_output)
        
        
        self._current_target=None
        self.add(self.output_pos)
        self.add(self.output_target)
        
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
            if type(v)== Waypoint:
                self._current_target=v
                
                
        
                
    def update_output(self):
        wp = self._session.get_current_waypoint()
        
        s = 'Your Position\n'
        s += wp.strlatlon()+'\n'
        s += 'Alt: %.0f m\n'%wp.alt
        s += 'Speed: %.5f m/s\n'%wp.speed
        s += 'Heading: %.1f °'%wp.heading 
        self.output_pos.set_text(s)
        
        if self._current_target!=None:
            dist_to_target=wp.distance_to(self._current_target)*1000
            head_to_target= wp.heading_to(self._current_target)
            s = 'Target\n'
            s += self._current_target.strlatlon()+'\n'
            s += 'Distance: %.0f m\n'%dist_to_target 
            s += 'Direction %.1f°\n'%head_to_target
            relative_direction=head_to_target-wp.heading
            s += 'Turn %s by '%('left','right')[relative_direction>0]
            s += '%.1f°\n'%abs(relative_direction)
            self.output_target.set_text(s)
        
        return 1
