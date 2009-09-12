#!/bin/bash
rfcomm bind rfcomm0  00:11:67:80:AE:EE
gpsd /dev/rfcomm0 

