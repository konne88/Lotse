#!/bin/bash
rfcomm bind rfcomm0  00:11:67:80:AE:EE
sudo gpsd /dev/rfcomm0 

