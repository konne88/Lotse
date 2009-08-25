from waypoint import Waypoint
from session import Session
from lib.event import Event

class Logger(object):
    def __init__(self, session):
        self._session = session
        self._running = False
        self.status_changed = Event()
        self.error_encountered = Event()

    def start(self):
        if self._running == False:
            self._session.position_changed += self.on_position_changed
            self._running = True
            self.status_changed(self)

    def stop(self):
        if self._running == True:    
            self._session.position_changed -= self.on_position_changed
            self._running = False
            self.status_changed(self)

    def get_running(self):
        print 'is running'
        return self._running

    running = property(get_running)  

    def get_name(self):
        raise NotImplementedError

    def on_position_changed(self):
        raise NotImplementedError

