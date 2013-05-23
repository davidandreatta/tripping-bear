README - png2poly

png2poly converts single *.KMZ in multiple KML with polygons

Usage: png2poly.py -i <Kmz input file> [optional: -x <img xsize> -y <img ysize>]

<Kmz input file> : name of the kmz file (place in the same directory of the executable)
<img xsize> :  width of the png image (default 1680 px)
<img ysize> :  height of the png image (default 1050 px)


The program gives the following output:

<CURR_path>\<Kmz input file>\ : extracted kmz file (doc.kml + files/*.png)
<CURR_path>\<Kmz input file>\output\kml : kml files with polygons 
<CURR_path>\<Kmz input file>\output\<Kmz input file>\ : .shp files

