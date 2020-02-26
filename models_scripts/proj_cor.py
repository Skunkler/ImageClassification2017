import arcpy
from arcpy import env

inDir=raw_input("Please enter directory: ")



env.workspace = inDir

rasters = arcpy.ListRasters()


dsc = arcpy.Describe(r'R:\Image_ClarkCounty\2017\ClarkCounty_Collection\122\o12204.tif')
coord_sys = dsc.spatialReference

for raster in rasters:
    print "correcting projected coordinate system of " + str(raster)
    arcpy.DefineProjection_management(raster, coord_sys)
    
