from coordinates import Coordinates

class Position(Coordinates):
    def __init__(self, lat=0,lon=0, alt=0,head=0, speed=0, time=0, fix=0, satellites = []):
        super(Position, self).__init__(lat,lon,alt)
        self.heading = head
        self.speed = speed
        
        self.time = time
        self.fix = fix
        self.satellites = satellites

    def relative_heading_to(self,coord):
        return self.heading_to(coord) - self.heading
        
    def get_satellites_used(self):
        c = 0
        for s in self.satellites:
            if s.used:
                c+=1
                
        return c
    
    satellites_used = property(get_satellites_used)
        
    def judge_quality(self):
        "Judge Quality 0.0 to 1.0" 
        if self.fix == 2: return 0.2
        elif self.fix == 3:
            return -1.0/(float(self.satellites_used)-1.0)+1.0
        else: return 0
