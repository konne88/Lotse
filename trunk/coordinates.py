#!/usr/bin/env python
#coding=utf-8

from math import *

class Coordinates(object):
    def __init__(self,lat, lon, alt):
        self.lat = lat
        self.lon = lon
        self.alt = alt
    
    def heading_to(self,coord):
        y = sin(radians(coord.lon-self.lon)) * cos(radians(coord.lat))
        x = cos(radians(self.lat)) * sin(radians(coord.lat)) \
          - sin(radians(self.lat)) * cos(radians(coord.lat)) \
          * cos(radians(coord.lon-self.lon))
        
        return (degrees(atan2(y, x))+360) % 360

    def distance_to(self, coord):
        R = 6371
        d = acos(sin(radians(self.lat))*sin(radians(coord.lat)) \
          + cos(radians(self.lat))*cos(radians(coord.lat)) \
          * cos(radians(coord.lon-self.lon))) * R;
        return d
    
    def strlatlon(self):
        s = ""
        
        for v,h,f in ((self.lat,('N','S'),True),(self.lon,('E','W'),False)):
            degreeF = abs(v)
            degree = int(degreeF)
            minutesF = (degreeF - degree)*60
            minutes = int(minutesF)
            secondsF = (minutesF - minutes)*60
                        
            s += '%d°%d\'%.3f" %s'%(degree,minutes,secondsF,h[v<0])
                        
            if f:
                s+=", "

        return s

    @staticmethod
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
        if len(split)>2:
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
                while not s[0].isdigit() and s[0] !="+" and s[0]!="-" and s[0]!="." and s[0]!=",":
                    s = s[1:]
                
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
                
                sp = s.partition("\″")
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
    
    
