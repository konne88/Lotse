import xml.dom.minidom as xml
import string
import gtk
import os
from waypoint import Waypoint
from session import Source

class WaypointLoader(object):
    def __init__(self, wpList):
        self.wpList=wpList
    
    def load_from_file(self, filename):
        try:
            file = open(filename, 'r')
        
            doc = xml.parse(file)
            currentSource = Source(os.path.basename(filename))
            sourceIter = self.wpList.append(None,(currentSource,))       
            
            if doc.documentElement.tagName == 'gpx':
                waypoints = doc.getElementsByTagName('wpt')                
                for waypoint in waypoints:                    

                        wp=Waypoint()
                        wp.lat=float(waypoint.getAttribute('lat'))
                        wp.lon=float(waypoint.getAttribute('lon'))  
                        
                        alt_element = \
                            waypoint.getElementsByTagName('ele')
                        if alt_element.length > 0:
                            wp.alt=float(alt_element[0].firstChild.data)

                        name_element = \
                            waypoint.getElementsByTagName('name')
                        if name_element.length > 0:
                            wp.name = string.strip(name_element[0].firstChild.data)
                        
                        
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

            return False
