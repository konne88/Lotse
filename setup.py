#!/usr/bin/env python

from distutils.core import setup

setup(name='lotse',
      version='0.1',
      description='GPS Geocaching tool',
      author='Konstantin Weitz, Niklas Schnelle',
      author_email='niklas@komani.de',
      url='http://github.com/konne88/Lotse',
      packages=['session', 'gtkgui','lib'],
      scripts=['lotse']
      )
