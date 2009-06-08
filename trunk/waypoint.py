from coordinates import Coordinates

class Waypoint(Coordinates):
    def __init__(self, lat,lon=0, alt=0,head=0, speed=0, name=''):
        super(Waypoint, self).__init__(lat,lon,alt)
        self.heading = head
        self.speed = speed
        self.name = name
