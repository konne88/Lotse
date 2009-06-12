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
 
    def foreach_wpListElement_persist(self, model, path, iter, doc):
        curr_object=model.get_value(iter,0)#We only have 1 column
        curr_section=self._curr_xml_section
        
        if issubclass(type(curr_object),Source):
            #Add Sources Section
            self._curr_xml_section=append_element(doc,curr_section,curr_object.name)

        elif issubclass(type(curr_object),Waypoint):
            append_element_with_data(doc,curr_section,'name',curr_object.name)
            append_element_with_data(doc,curr_section,'latitude',curr_object.lat)
            append_element_with_data(doc,curr_section,'longitude',curr_object.lon)
            append_element_with_data(doc,curr_section,'altitude',curr_object.alt)
           
    
    def save_persistent(self):
        # writexml(self, writer, indent='', addindent='', newl='', encoding=None)
        file = open('persist.xml', 'w')
        doc = create_doc('session')
        root = doc.documentElement
        
        #Add WaypointList Section
        self._curr_xml_section=append_element(doc,root,'waypoint_list')
        
        self.wpList.foreach(self.foreach_wpListElement_persist, doc )
       
        doc.writexml(file,' ',' ','\n', 'UTF-8')
        

