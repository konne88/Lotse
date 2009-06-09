import gps
import gtk
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
    
    def get_current_waypoint(self):
        self._gps.query('admosy')
        
        wp = Waypoint(
            self._gps.fix.latitude,
            self._gps.fix.longitude,
            self._gps.fix.altitude,
            self._gps.fix.speed,
            self._gps.fix.track
        )
        
        return wp

