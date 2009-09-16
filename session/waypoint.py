from coordinates import Coordinates

class Waypoint(Coordinates):
    def __init__(self, lat=0,lon=0, alt=0, name='Unnamed'):
        super(Waypoint, self).__init__(lat,lon,alt)
        self.name = name
    
    def set_coordinates(self, coord):
        self.lat = coord.lat
        self.lon = coord.lon
        self.alt = coord.alt
