import gtk
import gobject
import xml.dom.minidom as xml
import string
import os 

import lib.easyxml as easyxml
import lib.gps as gps
from lib.event import Event

from waypoint import Waypoint
from position import Position

class Source(object):
    def __init__(self,name):
        self.name = name
    
    def __str__():
        return self.name

class Session(object):
    def __init__(self):
        self._gps = gps.gps()
        self.wpList = gtk.TreeStore(object)
                
        self.settingsdir = os.path.expanduser("~/.lotse")
        if not os.path.exists(self.settingsdir):
            os.makedirs(self.settingsdir)

        self.load_persistent()
        
        self._position = Position() # Should not be none to not cause invalid calls
        self._sleek_position = Position()
        self._target = Waypoint()
        
        self.position_changed = Event()
        self.target_changed = Event()
        self._time = 0
        
        self.update()
        gobject.timeout_add(400, self.update)
        
    
    def get_sleek_position(self):
        return self._sleek_position
    
    sleek_position = property(get_sleek_position)
    
    def get_position(self):
        return self._position
    
    position = property(get_position)
    
    def get_time(self):
        return self._time
        
    time = property(get_time)
    
    def get_fix(self):
        return self._fix
        
    fix = property(get_fix)
       
    def get_target(self):
        return self._target
        
    def set_target(self, value):
        self._target = value
        self.target_changed()
        
    target = property(get_target,set_target)

    def update(self):
        self._gps.query('admosy')
        if self._time != self._gps.fix.time: 
            self._time = self._gps.fix.time   
            self._fix = self._gps.fix.mode     
            
            self._position = Position(
                self._gps.fix.latitude,
                self._gps.fix.longitude,
                self._gps.fix.altitude,
                self._gps.fix.track,
                self._gps.fix.speed,
            )
            
            if self._gps.fix.speed<1.0:
                ihead=self.sleek_position.heading
            else:
                ihead=self._gps.fix.track
            
            if ihead != ihead:  #NaN
                ihead = 0
            
            self._sleek_position = Position(
                self._gps.fix.latitude,
                self._gps.fix.longitude,
                self._gps.fix.altitude,
                ihead,
                self._gps.fix.speed,
            )
            
            
            
            self.position_changed()
           
        return True
 
    def foreach_wpListElement_persist(self, model, path, iter,( doc, waypoint_section)):
        curr_object = model.get_value(iter,0)#We only have 1 column
        curr_section = self._curr_xml_section
        
        if issubclass(type(curr_object),Source):
            #Add Sources Section
            self._curr_xml_section=easyxml.append_element(doc, waypoint_section,'source','type',curr_object.name)

        elif issubclass(type(curr_object),Waypoint) and curr_section != None:
            wp_xml=easyxml.append_element(doc,curr_section,'wp')
            easyxml.append_element_with_data(doc,wp_xml,'name',curr_object.name)
            easyxml.append_element_with_data(doc,wp_xml,'latitude',curr_object.lat)
            easyxml.append_element_with_data(doc,wp_xml,'longitude',curr_object.lon)
            easyxml.append_element_with_data(doc,wp_xml,'altitude',curr_object.alt)
           
    def save_persistent(self):
        # writexml(self, writer, indent='', addindent='', newl='', encoding=None)
        file = open(os.path.join(self.settingsdir,'persist.xml'), 'w')
        doc = easyxml.create_doc('session')
        root = doc.documentElement
        self._curr_xml_section=None
        #Add WaypointList Section
        waypoint_section=easyxml.append_element(doc,root,'waypoints')
        
        self.wpList.foreach(self.foreach_wpListElement_persist,( doc, waypoint_section ))
       
        doc.writexml(file,' ',' ','\n', 'UTF-8')

    def load_persistent(self):
        try:

            file = open(os.path.join(self.settingsdir,'persist.xml'), 'r')
        
            doc = xml.parse(file)
            if doc.documentElement.tagName == 'session':
                waypoint_list = doc.getElementsByTagName('waypoints')[0]
                sources = waypoint_list.getElementsByTagName('source')
                for source in sources:
                    currentSource = Source(source.getAttribute('type'))
                    if currentSource.name == "Manual Waypoints":
                        self.manualSource = currentSource
                        
                    sourceIter = self.wpList.append(None,(currentSource,))                                   

                    waypoints=source.getElementsByTagName('wp')                    
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
                        #print '---'+wp.name
                        #Append Waypoint to correct Source Object
                        self.wpList.append(sourceIter,(wp,))
                        
            #if document is empty or contains garbage raise IOError   after cleaning up                    
            else:
                doc.unlink()
                file.close()
                raise IOError
                
            doc.unlink()
            file.close()
            return True
        except(IOError):
            #The File is not available for reading so insert standard Source into the list
            currentSource = Source('Manual Waypoints')
            self.manualSource = currentSource
            self.wpList.append(None,(currentSource,))
            return False
