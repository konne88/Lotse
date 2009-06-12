import gps
import gtk
from waypoint import Waypoint
from xml.parsers.expat import ExpatError
import xml.dom.minidom as xml

""" Some XML Document Helper Functions that have no better place"""
def append_element(doc,parent,name):
    n = doc.createElement(name)
    parent.appendChild(n)
    return n

def append_element_with_data(doc,parent,name,data):
    n = append_element(doc,parent,name)
    t = doc.createTextNode(str(data))
    n.appendChild(t)
    return n

def create_doc(root):
    impl = xml.getDOMImplementation()
    doc = impl.createDocument(None, root, None)
    return doc



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
    
    def get_current_waypoint(self):
        self._gps.query('admosy')
        
        wp = Waypoint(
            self._gps.fix.latitude,
            self._gps.fix.longitude,
            self._gps.fix.altitude,
            self._gps.fix.track,
            self._gps.fix.speed
        )
        
        return wp
    def save_persistent(self):
        # writexml(self, writer, indent='', addindent='', newl='', encoding=None)
        file = open('persist.xml', 'w')
        doc = create_doc('session')
        root = doc.documentElement
        
        #Add WaypointList Section
        waypoint_list_section=append_element(doc,root,'waypoint_list')

        
        l = self.wpList
        i = l.get_iter_first()
        while i is not None:
            curr_object=l.get_value(i,0) #We only have 1 column
            print curr_object.name
            if issubclass(type(curr_object),Source):
                #Add Sources Section
                curr_source_section=append_element(doc,waypoint_list_section,'manual_source')

            elif issubclass(type(curr_object),Waypoint):
                append_element_with_data(doc,curr_source_section,'name',curr_object.name)
                append_element_with_data(doc,curr_source_section,'latitude',curr_object.lat)
                append_element_with_data(doc,curr_source_section,'longitude',curr_object.lon)
                append_element_with_data(doc,curr_source_section,'altitude',curr_object.alt)
       
            
            i = l.iter_next(i);  
        doc.writexml(file,' ',' ','\n', 'UTF-8')
        

