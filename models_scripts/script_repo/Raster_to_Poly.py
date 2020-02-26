#This script was written by Warren Kunkler in support of the Clark County Image Classification Project for 2016
#The goal of this project is to support the Water Smart Landscape project
#The output of this script is the vectorization of the thematic classified raster images that were created by the Softmax Regression Classifier


import arcpy, sys, datetime, time, os, string
from arcpy import env



env.overwriteOutput = True
#workspace directory pointing to cleaned thematically classified imagery
ws = r''
env.workspace = ws



#define rasters and output workspace
output = r''
rasters = arcpy.ListRasters("*","*")

#loop through rasters and convert each one to a polygon
for raster in rasters:
    try:
        print "converting: ", raster, " to polygon"
        Polys = output + '\\' + raster[:-4]   
        arcpy.RasterToPolygon_conversion(raster, Polys, "NO_SIMPLIFY", "VALUE")
    except:

        print arcpy.GetMessages(2)
       
