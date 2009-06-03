#!/usr/bin/env python
#coding=utf-8

from math import *

class Coordinates:
	def __init__(self,lat, lon, alt):
		self.lat = lat
		self.lon = lon
		self.alt = alt
	
	def bearing(self,coord):
		y = sin(radians(coord.lon-self.lon)) * cos(radians(coord.lat))
		x = cos(radians(self.lat))*sin(radians(coord.lat))-sin(radians(self.lat))*cos(radians(coord.lat))*cos(radians(coord.lon-self.lon))
		return (degrees(atan2(y, x))+360) % 360

	def distance(self, coord):
		R = 6371
		d = acos(sin(radians(self.lat))*sin(radians(coord.lat))+cos(radians(self.lat))*cos(radians(coord.lat))*cos(radians(coord.lon-self.lon))) * R;
		return d
	
	@staticmethod
	def parse_string(co):
		lat = 0
		lon = 0
		
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
				degree = 0
				minutes = 0
				seconds = 0
				
				# remove all leading non digits
				while not s[0].isdigit():
					s = s[1:]
				
				sp = s.partition("°")
				if(sp[1] != ""):
					degree = float(sp[0])
					s = sp[2]
				else:
					s = sp[0]
				
				sp = s.partition("'")
				if(sp[1] != ""):
					minutes = float(sp[0])
					s = sp[2]
				else:
					s = sp[0]
				
				sp = s.partition("′")
				if(sp[1] != ""):
					minutes = float(sp[0])
					s = sp[2]
				else:
					s = sp[0]
				
				sp = s.partition("`")
				if(sp[1] != ""):
					minutes = float(sp[0])
					s = sp[2]
				else:
					s = sp[0]
				
				sp = s.partition("\"")
				if(sp[1] != ""):
					seconds = float(sp[0])
					s = sp[2]
				else:
					s = sp[0]
					
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
				
			++i
			
			print degree
			print minutes
			print seconds
			print lat
			print lon
			
		return Coordinates(lat,lon,0)

if __name__ == "__main__":
	print Coordinates.parse_string("Lat = 47° 25\" Nord, Lon = 010° 59' 3 0\" Ost")