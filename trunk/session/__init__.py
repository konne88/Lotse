import gtk
import gobject
import xml.dom.minidom as xml

import lib.easyxml as easyxml
import lib.gps as gps
from lib.event import Event

from waypoint import Waypoint

class Source(object):
    def __init__(self,name):
        self.name = name
    
    def __str__():
        return self.name

class Session(object):
    def __init__(self):
        self._gps = gps.gps()
        self.wpList = gtk.TreeStore(object)
        self.manualSource = Source("Manual Waypoints")
        self.wpList.append(None,(self.manualSource,))
        
        self._position = None
        self._target = None
        
        self.position_changed = Event()
        self.target_changed = Event()
        
        self.update_position()
        gobject.timeout_add(100, self.update_position)
    
    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, value):
        self._position = value
        self.position_changed()
        
    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        self._target = value
        self.target_changed()
    
    def update_position(self):
        self._gps.query('admosy')
        
        self.position = Waypoint(
            self._gps.fix.latitude,
            self._gps.fix.longitude,
            self._gps.fix.altitude,
            self._gps.fix.track,
            self._gps.fix.speed
        )
                
        return True
 
    def foreach_wpListElement_persist(self, model, path, iter, doc):
        curr_object = model.get_value(iter,0)#We only have 1 column
        curr_section = self._curr_xml_section
        
        if issubclass(type(curr_object),Source):
            #Add Sources Section
            self._curr_xml_section=easyxml.append_element(doc,curr_section,curr_object.name)

        elif issubclass(type(curr_object),Waypoint):
            easyxml.append_element_with_data(doc,curr_section,'name',curr_object.name)
            easyxml.append_element_with_data(doc,curr_section,'latitude',curr_object.lat)
            easyxml.append_element_with_data(doc,curr_section,'longitude',curr_object.lon)
            easyxml.append_element_with_data(doc,curr_section,'altitude',curr_object.alt)
           
    def save_persistent(self):
        # writexml(self, writer, indent='', addindent='', newl='', encoding=None)
        file = open('persist.xml', 'w')
        doc = easyxml.create_doc('session')
        root = doc.documentElement
        
        #Add WaypointList Section
        self._curr_xml_section=easyxml.append_element(doc,root,'waypoints')
        
        self.wpList.foreach(self.foreach_wpListElement_persist, doc )
       
        doc.writexml(file,' ',' ','\n', 'UTF-8')

    def load_persistent(self):
        try:
            file = open('persist.xml', 'r')
        
            doc = xml.parse(file)
            assert doc.documentElement.tagName == 'session'
            waypoint_list = doc.getElementsByTagName('waypoints')[0]
            sources = waypoint_list.getElementsByTagName('source')
            for source in sources:
                if source.getAttribute('type') == 'manual': 
                    self.manualSource = Source('manual')
                    waypoints=source.getElementsByTagName('wp')
                    self.wpList.append(None,(self.manualSource,))
                    for waypoint in waypoints:
                        wp=Waypoint()
                        name_element = \
                            waypoint.getElementsByTagName('name')[0]
                        lat_element = \
                            waypoint.getElementsByTagName('latitude')[0]
                        lon_element = \
                            waypoint.getElementsByTagName('longitude')[0]
                        alt_element = \
                            waypoint.getElementsByTagName('altitude')[0]
                                
                        wp.name = string.strip(name_element.firstChild.data)
                        wp.lat=float(lat_element.firstChild.data)
                        wp.lon=float(lon_element.firstChild.data)
                        wp.alt=float(alt_element.firstChild.data)
                        
                        m = self.wpList
                        
                        i = m.get_iter_first()
                        while i is not None:
                            if m.get_value(i,0) == self.manualSource:
                                new_row = m.append(i,(wp,))                                    
                            i = m.iter_next(i);
            
            doc.unlink()
            file.close()
            return True
        except(IOError):
            return False
