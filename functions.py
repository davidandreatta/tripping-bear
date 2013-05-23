#!/usr/bin/python

####################################################################################################
# Function file of png2poly.py - Convert single *.KMZ in multiple KML with polygons
#	
#	CalcWorldFile creates world file for the png image starting from lat,lon,image size 
# 
#	info: david.andreatta@brennercom.it
#####################################################################################################

import os
import subprocess
import commands
import sys
import socket
import tarfile
import zipfile
import datetime
import time
import email
import logging
import subprocess



def CalcWorldFile(lat1,lon1,lat2,lon2,xsize,ysize,fname):

	lat1 = float(lat1)
	lon1 = float(lon1)
	lat2 = float(lat2)
	lon2 = float(lon2)

	if lon1 < lon2 :
		t = +lon1
		lon1 = lon2
		lon2 = t

	ppx = ( lon1 - lon2 ) / xsize

	if lat1 > lat2 :
		t = +lat1
		lat1 = lat2
		lat2 = t
	ppy = ( lat1 - lat2 ) / ysize

	lon2 = lon2 + ( ppx / 2 )
	lat2 = lat2 + ( ppy / 2 )

	wf = []

	wf.append(ppx)
	wf.append('0.00000')
	wf.append('0.00000')
	wf.append(ppy)
	wf.append(lon2)
	wf.append(lat2)


	wFile = open(fname,'a')
	i = 0
	
	while i < len(wf):
		wFile.writelines('%s\n' % wf[i])
		i = i+1
	wFile.close()



