#!/usr/bin/python

####################################################################################################
# Python Script - Convert single *.KMZ in multiple KML with polygons
#
# STEP:
#
#	1 - extract KMZ
#	2 - recover coordinates LatLonBox, creating world files (*.pgw), following
#		http://egb13.net/2009/03/worldfile-calculator/ . Javascript can be found in js/worldfile.js
#	3 - gdal_polygonize.py conversion from  RASTER to VECTOR file (shapefile) via QGIS
#	4 - conversion / saving in KML
#
#	info: david.andreatta@brennercom.it
#####################################################################################################

#IMPORT SECTION

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
import re
import getopt
import shutil
from xml.dom.minidom import parse
from xml.dom.minidom import parseString
from PIL import Image
from functions import CalcWorldFile

#####################################################################################################
# Functions
#####################################################################################################
#Checking if the directory exists

def check_dir(dir):
        if not os.path.exists(dir):
               os.makedirs(dir)
        else:
        	shutil.rmtree(dir)
        	os.makedirs(dir)

# Extracting KMZ

def xtrctKMZ (dir,fname):
		z = zipfile.ZipFile(os.path.join(dir,fname))
		z.extractall(os.path.join(dir,fname.rstrip('.kmz')))


#####################################################################################################
# Script
#####################################################################################################

#####################################################################################################
# Help Menu
#####################################################################################################

argv = len(sys.argv)

if ( argv == 1 ):
	print 'Usage: png2poly.py -i <Kmz input file>' 
	sys.exit()

for arg in sys.argv[1:]:
	try:
		opts, args = getopt.getopt(sys.argv[1:],"hi:x:y:")
	except getopt.GetoptError as err:
		print 'Usage: png2poly.py -i <Kmz input file>'
		sys.exit()
	
	if len(opts) == 0:
		print 'Usage: png2poly.py -i <Kmz input file>'
		sys.exit()

	for opt,arg in opts:
		if opt == '-h':
			print 'Usage: png2poly.py -i <Kmz input file>'
			sys.exit()
		elif opt in ("-i"):
			inFileKMZ = arg
			try:
				f = open(os.path.abspath(arg), 'r')
			except IOError:
				print 'File non presente\nUsage: png2poly.py -i <Kmz input file>'
				sys.exit()	
		
#####################################################################################################

curDir = commands.getoutput('pwd')
inFileKMZ = os.path.basename(os.path.abspath(inFileKMZ)).rstrip('.kmz')	
inFileKML = os.path.join(curDir,inFileKMZ,'doc.kml')
pngDir = os.path.join(curDir,inFileKMZ,'files')

# creating output directory
outDir = os.path.join(curDir,inFileKMZ,'output')
outDirKml = os.path.join(curDir,inFileKMZ,'output','kml')
check_dir(os.path.join(curDir,inFileKMZ))
check_dir(outDir)
check_dir(outDirKml)
inFileKMZ = inFileKMZ + '.kmz'

# Extracting KMZ
xtrctKMZ(curDir,inFileKMZ)


# Parsing KML file, extracting array coordinates (north,south,east,west)
North = []
South = []
East = []
West = []
img = []


i = 0

dom1 = parse(inFileKML)

for direction in 'north','south','east','west':
	for node in dom1.getElementsByTagName(direction):
		if direction == 'north':
			North.append(node.firstChild.toxml())
		if direction == 'south':
			South.append(node.firstChild.toxml())
		if direction == 'east':
			East.append(node.firstChild.toxml())
		if direction == 'west':
			West.append(node.firstChild.toxml())

for node in dom1.getElementsByTagName('href'):
	z = node.firstChild.toxml()
	if not "http" in z:
		img.append(z)

while i < len(img):
	im = Image.open(os.path.join(curDir,inFileKMZ.rstrip('.kmz'),img[i]))
	xsize = im.size[0]
	ysize = im.size[1]
	result = re.search('files/(.*).png', img[i])
	fname = result.group(1)
	CalcWorldFile(North[i],East[i],South[i],West[i],xsize,ysize,os.path.join(pngDir,'%s.pgw' % fname))
	i = i + 1


# Getting files and converting to KML through gdal_polygonize and ogr2ogr

for files in os.listdir(pngDir):
	if files.endswith(".png"):
		fname = files.rstrip('.png')

		pngPath = os.path.join(pngDir,'%s.png' % fname)
		outPath = os.path.join(outDir,fname)
		kmlPath = os.path.join(outDirKml,'%s.kml' % fname)

		os.system('gdal_polygonize.py %s -f "ESRI Shapefile" %s %s' % (pngPath, outPath, fname))
		os.system('ogr2ogr -f KML %s %s' % (kmlPath, os.path.join(outPath,'%s.shp' % fname)))

quit()
