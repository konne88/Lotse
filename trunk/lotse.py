#!/usr/bin/env python
#import osso
#import hildon
import gtk
import gobject

import gps, os, time, sys
from math import *

class coordinates:
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




        #session.query('admosy')
        ## a = altitude, d = date/time, m=mode,
        ## o=postion/fix, s=status, y=satellites

        #print
        #print ' GPS reading'
        #print '----------------------------------------'
        #print 'latitude    ' , session.fix.latitude
        #print 'longitude   ' , session.fix.longitude
        #print 'time utc    ' , session.utc, session.fix.time
        #print 'altitude    ' , session.fix.altitude
        ##print 'eph         ' , session.fix.eph
        ##print 'epv         ' , session.fix.epv
        ##print 'ept         ' , session.fix.ept
        #print 'speed       ' , session.fix.speed
        #print 'climb       ' , session.fix.climb
	#print 'track       ' , session.fix.track
	#print 'status	   ' , session.status       
	#print
        ##print ' Satellites (total of', len(session.satellites) , ' in view)'
        ##for i in session.satellites:
        ##    print '\t', i
	#if len(sys.argv)>3:
		#altitude=float(sys.argv[3])
	#else: 
		#altitude=0
	
	#coord1 = coordinates(session.fix.latitude, session.fix.longitude, session.fix.altitude)
	#coord2 = coordinates(float(sys.argv[1]),float(sys.argv[2]), altitude)
	
	#print 'Bearing to point (in degrees)',bearing(coord1,coord2)
	#print 'Distance to point (in m)', distance(coord1,coord2)*1000
    #    time.sleep(1)

def update_widget(session, infolabel):	
    session.query('admosy')
    
    infostring=''
    infostring+='Status: '+str(session.status)+'\n'
    infostring+='Latitude: %.5f'%session.fix.latitude+'\n'
    infostring+='Longitude: %.5f'%session.fix.longitude+'\n'
    infostring+='Speed: %.5f'%session.fix.speed+' m/s\n'
    infostring+='Track: %.5f'%session.fix.track+'\n'
    infostring+='Altitude: %.0f'%session.fix.altitude+' m\n'

    infostring+='Time (UTC): '+session.utc+'\n'

    infolabel.set_text(infostring)
    return 1
 
def window_destroy(widget, data=None):
    gtk.main_quit()

def main():
 #   osso_c = osso.Context("osso_test_app", "0.0.1", False)
  #  program  = hildon.Program()
  #  window = hildon.Window()
    window = gtk.Window()
    label = gtk.Label("")
    label.set_text('test')
    window.add(label)
    session = gps.gps()
    gobject.timeout_add(100, update_widget, session, label)
    window.show_all()
    window.connect('destroy', window_destroy)
    gtk.main()

main()
