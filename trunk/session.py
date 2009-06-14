import gps
import gtk
import string
from waypoint import Waypoint
from xml.parsers.expat import ExpatError
import xml.dom.minidom as xml

""" Some XML Document Helper Functions that have no better place"""
def append_element(doc,parent,name,attribute_name=None,attribute_value=None):
    n = doc.createElement(name)
    if attribute_name!=None:
        n.setAttribute(attribute_name, attribute_value)
    
    parent.appendChild(n)
    return n

def append_element_with_data(doc,parent,name,data, attribute_name=None, attribute_value=None):
    n = append_element(doc, parent,name, attribute_name, attribute_value)
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
        if not self.load_persistent():
            self.manualSource = Source("manual")
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
            self._curr_xml_section=append_element(doc,curr_section,'source','type',curr_object.name)

        elif issubclass(type(curr_object),Waypoint):
            waypoint_element=append_element(doc,curr_section,'wp')
            append_element_with_data(doc,waypoint_element,'name',curr_object.name)
            append_element_with_data(doc,waypoint_element,'latitude',curr_object.lat)
            append_element_with_data(doc,waypoint_element,'longitude',curr_object.lon)
            append_element_with_data(doc,waypoint_element,'altitude',curr_object.alt)
           
    
    def save_persistent(self):
        # writexml(self, writer, indent='', addindent='', newl='', encoding=None)
        file = open('persist.xml', 'w')
        doc = create_doc('session')
        root = doc.documentElement
        
        #Add WaypointList Section
        self._curr_xml_section=append_element(doc,root,'waypoint_list')
        
        self.wpList.foreach(self.foreach_wpListElement_persist, doc )
       
        doc.writexml(file,' ',' ','\n', 'UTF-8')
        file.close()
        
    def load_persistent(self):
        try:
            file = open('persist.xml', 'r')
        
            doc = xml.parse(file)
            assert doc.documentElement.tagName == 'session'
            waypoint_list = doc.getElementsByTagName('waypoint_list')[0]
            sources = waypoint_list.getElementsByTagName('source')
            for source in sources:
                if source.getAttribute('type') == 'manual': 
                    self.manualSource = Source('manual')
                    waypoints=source.getElementsByTagName('wp')
                    self.wpList.append(None,(self.manualSource,))
                    for waypoint in waypoints:
                                wp=Waypoint()
                                name_element =\
                                 waypoint.getElementsByTagName('name')[0]
                                lat_element =\
                                 waypoint.getElementsByTagName('latitude')[0]
                                lon_element =\
                                 waypoint.getElementsByTagName('longitude')[0]
                                alt_element =\
                                 waypoint.getElementsByTagName('altitude')[0]
                                
                                wp.name=string.strip(name_element.firstChild.data)
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
            
        
        

