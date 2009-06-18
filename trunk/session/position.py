from coordinates import Coordinates

class Position(Coordinates):
    def __init__(self, lat=0,lon=0, alt=0,head=0, speed=0):
        super(Position, self).__init__(lat,lon,alt)
        self.heading = head
        self.speed = speed

    def relative_heading_to(coord):
        return heading_to(coord) - heading