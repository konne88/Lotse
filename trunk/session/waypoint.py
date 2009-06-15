from coordinates import Coordinates

class Waypoint(Coordinates):
    def __init__(self, lat=0,lon=0, alt=0,head=0, speed=0, name='Unnamed'):
        super(Waypoint, self).__init__(lat,lon,alt)
        self.heading = head
        self.iheading = head
        self.speed = speed
        self.name = name
        
