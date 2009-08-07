from waypoint import Waypoint
from session import Session

class Logger(object):
    def __init__(self, session):
        self._session = session
        self._started = False
        
    def start(self):
        if self._started == False:
            self._session.position_changed += self.on_position_changed
            self._started = True
    def stop(self):
        if self._started == True:    
            self._session.position_changed -= self.on_position_changed
            self._started = False
        
   
    def end(self):
        print "___END___"    
        
    def on_position_changed(self):
        print self._session.sleek_position.strlatlon()
        
        
        

