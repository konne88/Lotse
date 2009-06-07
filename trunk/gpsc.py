#!/usr/bin/env python
import gps, os, time, sys
from math import *

class Coordinates:
    def __init__(self,lat, lon, alt):
            # Sets all the properties
            self.lat = lat
            self.lon = lon
            self.alt = alt
 
    def bearing(coord1,coord2):
        y = sin(radians(coord2.lon-coord1.lon)) * cos(radians(coord2.lat))
        x = cos(radians(coord1.lat))*sin(radians(coord2.lat))-sin(radians(coord1.lat))*cos(radians(coord2.lat))*cos(radians(coord2.lon-coord1.lon))
        return (degrees(atan2(y, x))+360) % 360

    def distance(coord1, coord2):
        R = 6371
        d = acos(sin(radians(coord1.lat))*sin(radians(coord2.lat))+cos(radians(coord1.lat))*cos(radians(coord2.lat))*cos(radians(coord2.lon-coord1.lon))) * R;
        return d

session = gps.gps()

while 1:
        os.system('clear')
        session.query('admosy')
        # a = altitude, d = date/time, m=mode,
        # o=postion/fix, s=status, y=satellites

        print
        print ' GPS reading'
        print '----------------------------------------'
        print 'latitude    ' , session.fix.latitude
        print 'longitude   ' , session.fix.longitude
        print 'time utc    ' , session.utc, session.fix.time
        print 'altitude    ' , session.fix.altitude
        #print 'eph         ' , session.fix.eph
        #print 'epv         ' , session.fix.epv
        #print 'ept         ' , session.fix.ept
        print 'speed       ' , session.fix.speed
        print 'climb       ' , session.fix.climb
    print 'track       ' , session.fix.track
    print 'status      ' , session.status       
    print
        #print ' Satellites (total of', len(session.satellites) , ' in view)'
        #for i in session.satellites:
        #    print '\t', i
    if len(sys.argv)>3:
        altitude=float(sys.argv[3])
    else: 
        altitude=0
    
    coord1 = coordinates(session.fix.latitude, session.fix.longitude, session.fix.altitude)
    coord2 = coordinates(float(sys.argv[1]),float(sys.argv[2]), altitude)
    
    print 'Bearing to point (in degrees)',bearing(coord1,coord2)
    print 'Distance to point (in m)', distance(coord1,coord2)*1000
        time.sleep(1)


