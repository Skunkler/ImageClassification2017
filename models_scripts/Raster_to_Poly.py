#This script was written by Warren Kunkler in support of the Clark County Image Classification Project for 2016
#The goal of this project is to support the Water Smart Landscape project
#The output of this script is the vectorization of the thematic classified raster images that were created by the Softmax Regression Classifier


import arcpy, sys, datetime, time, os, string
from arcpy import env



env.overwriteOutput = True
#workspace directory pointing to cleaned thematically classified imagery
ws = r'D:\Clark_County_2017_ImageClassification_Project\Samples_models\AmendedData\eliminate'
env.workspace = ws

scratch = r"D:\Clark_County_2017_ImageClassification_Project\Samples_models\AmendedData\Scratch.gdb"


threeInchTiles = r"D:\Clark_County_2017_ImageClassification_Project\bookSecEdit\Veg_Sections_3in6in.shp"
arcpy.MakeFeatureLayer_management(threeInchTiles, 'threeInchLyr')

#define rasters and output workspace
finalOutput = r"D:\Clark_County_2017_ImageClassification_Project\Samples_models\AmendedData\RoughyPolys.gdb"
rasters = arcpy.ListRasters("*","*")

#loop through rasters and convert each one to a polygon
for raster in rasters:
    print raster
    try:
        print "converting: ", raster, " to polygon"
        Polys = scratch + '\\' + raster[:-4]   
        arcpy.RasterToPolygon_conversion(raster, Polys, "NO_SIMPLIFY", "VALUE")
        # 02/26/2019 dpw & wk IMAGE classes of 1 (non vegetation) and 5 (not classified) are not passed forward
        # from the raster to vector data.
        arcpy.MakeFeatureLayer_management(Polys, 'PolyLyr')
        arcpy.SelectLayerByAttribute_management('PolyLyr', 'NEW_SELECTION', ' "gridcode" in (1,5) ')
        arcpy.DeleteFeatures_management('PolyLyr')
        print "Clipping features"
        arcpy.SelectLayerByAttribute_management('threeInchLyr', 'NEW_SELECTION', "\"BOOKSEC_PT\" =" + ("'{}'".format(raster[:-4])))
        arcpy.Clip_analysis('PolyLyr', 'threeInchLyr', finalOutput + '\\' + raster[:-4])
    except:

        print arcpy.GetMessages(2)
       
