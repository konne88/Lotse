#!/usr/bin/env python
#coding=utf-8
#http://www.movable-type.co.uk/scripts/latlong.html

from math import *

EARTH_RADIUS =  6371 #in km

class Coordinates(object):
    def __init__(self,lat = 0, lon = 0, alt = 0):
        self._lat = lat
        self._lon = lon
        self.alt = alt
        self._strlatlon = ""
        self._updated()
        
    def get_lat(self):
        return self._lat
    
    def set_lat(self,val):
        self._updated()
        self._lat = val
        
    lat = property(get_lat,set_lat)
        
    def get_lon(self):
        return self._lon
    
    def set_lon(self,val):
        self._lon = val
        self._updated()
        
    lon = property(get_lon,set_lon)
    
    def _updated(self):
        s = ""
        for v,h,f in ((self.lat,('N','S'),True),(self.lon,('E','W'),False)):
            degreeF = abs(v)
            #Check whether degreeF is NaN this can happen when
            #starting shortly after gpsd
            if degreeF != degreeF:
                degreeF = 0.0
            degree = int(degreeF)
            minutesF = (degreeF - degree)*60
            minutes = int(minutesF)
            secondsF = (minutesF - minutes)*60
                        
            s += '%d°%d\'%.3f" %s'%(degree,minutes,secondsF,h[v<0])
                        
            if f:
                s+=", "

        self._strlatlon = s
    
    def set_from_heading_and_distance(self, coord, head, dist):
        "set everything with start coordinate, heading and distance"
        lat1 = radians(coord.lat)
        lon1 = radians(coord.lon)
        head = radians(head)
        sin_dist_earth = sin(dist/EARTH_RADIUS)
        cos_dist_earth = cos(dist/EARTH_RADIUS)
        
        lat2 = asin(sin(lat1)*cos_dist_earth+
            cos(lat1)*sin_dist_earth*cos(head))
        lon2 = lon1 + atan2(sin(head)*sin_dist_earth*cos(lat1),
            cos_dist_earth-sin(lat1)*sin(lat2))
        lon2 = (lon2+pi)%(2*pi)-pi
        
        self.lat = degrees(lat2)
        self.lon = degrees(lon2)
        
        self.alt = coord.alt    
  #var R = 6371; // earth's mean radius in km
  #var lat1 = this.lat.toRad(), lon1 = this.lon.toRad();
  #brng = brng.toRad();

  #var lat2 = Math.asin( Math.sin(lat1)*Math.cos(d/R) + 
                        #Math.cos(lat1)*Math.sin(d/R)*Math.cos(brng) );
  #var lon2 = lon1 + Math.atan2(Math.sin(brng)*Math.sin(d/R)*Math.cos(lat1), 
                               #Math.cos(d/R)-Math.sin(lat1)*Math.sin(lat2));
  #lon2 = (lon2+Math.PI)%(2*Math.PI) - Math.PI;  // normalise to -180...+180

  #if (isNaN(lat2) || isNaN(lon2)) return null;
  #return new LatLon(lat2.toDeg(), lon2.toDeg());

    
    def heading_to(self,coord):
        lat1 = radians(self.lat)
        lon1 = radians(self.lon)
        lat2 = radians(coord.lat)
        lon2 = radians(coord.lon)
        
        y = sin(lon2-lon1) * cos(lat2)
        x = cos(lat1) * sin(lat2) \
          - sin(lat1) * cos(lat2) \
          * cos(lon2-lon1)
        
        return (degrees(atan2(y, x))+360) % 360
        
    def distance_to(self, coord):
        lat1 = radians(self.lat)
        lon1 = radians(self.lon)
        lat2 = radians(coord.lat)
        lon2 = radians(coord.lon)
        
        d = acos(sin(lat1)*sin(lat2) \
          + cos(lat1)*cos(lat2) \
          * cos(lon2-lon1)) * EARTH_RADIUS;
        return d
    
    def strlatlon(self):
        return self._strlatlon

    def parse_string(co):
        lat = 0.0
        lon = 0.0
        
        co = co.lower()
        s = ""
        # remove all whitespaces from the string
        for c in co:
            if not c.isspace():
                s += c
        
        co = s
        
        split = co.split(",")
        if len(split)!=2: 
            raise ValueError()
        
        i = 0
        for s in split:
            try:
                if i == 0:
                    lat = float(s)
                else:
                    lon = float(s)
            except ValueError:
                degree = 0.0
                minutes = 0.0
                seconds = 0.0
                                
                # remove all leading non digits
                while not s[0].isdigit() and s[0] !="+" and s[0]!="-" and s[0]!=".":
                    s = s[1:]
                    if s == "":
                        raise ValueError()
                
                sp = s.partition("°")
                if(sp[1] != ""):
                    degree = float(sp[0])
                    s = sp[2]
                
                sp = s.partition("'")
                if(sp[1] != ""):
                    if not (len(sp[2]) > 0 and sp[2][0] == "'"):
                        minutes = float(sp[0])
                        s = sp[2]
                
                sp = s.partition("′")
                if(sp[1] != ""):
                    minutes = float(sp[0])
                    s = sp[2]
                
                sp = s.partition("`")
                if(sp[1] != ""):
                    minutes = float(sp[0])
                    s = sp[2]
                
                sp = s.partition("\"")
                if(sp[1] != ""):
                    seconds = float(sp[0])
                    s = sp[2]
                
                sp = s.partition("″")
                if(sp[1] != ""):
                    seconds = float(sp[0])
                    s = sp[2]
                
                sp = s.partition("''")
                if(sp[1] != ""):
                    seconds = float(sp[0])
                    s = sp[2]
                
                if len(s) > 0:
                    s = s[0]
                else:
                    s = ""
                
                val = degree+(minutes+seconds/60)/60
                
                if s == "n":
                    lat = val
                elif s in ["o","e"]:
                    lon = val
                elif s == "s":
                    lat = val * -1
                elif s == "w":
                    lon = val * -1
                elif i == 0:
                    lat = val
                else:
                    lon = val
                
            i=i+1
            
        return Coordinates(lat,lon,0)
    
    parse_string = staticmethod(parse_string)
    
if __name__ == "__main__":
    c1 = Coordinates.parse_string("Lat = -47° 25\" Nord,Lon = 010° 59' 3 0\" w")
    c2 = Coordinates.parse_string("48° 45′ 20.6″ N, 9° 11′ 24.8″ E")
    
    print c1.strlatlon()
    print c2.strlatlon()
    print c1.distance_to(c2) , "Km"
    print "------------------"
    
    c1 = Coordinates.parse_string("-48.168991,11.5768")
    c2 = Coordinates.parse_string("-48.167288,11.575706")
    
    print c1.strlatlon()
    print c2.strlatlon()
    print c1.distance_to(c2)*1000 , "m"
    
    
