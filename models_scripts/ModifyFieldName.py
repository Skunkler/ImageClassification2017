import arcpy
from arcpy import env

env.workspace = raw_input("Please enter fgdb")

fcs = arcpy.ListFeatureClasses()

for fc in fcs:
    print "changing field name for " + fc
    arcpy.AlterField_management(fc, fc[:-4] + 'APN', fc[:-6] + 'APN')
    arcpy.AlterField_management(fc, fc[:-4] + 'Shape_Area', fc[:-6] + 'Shape_Area')
    arcpy.Rename_management(fc, fc[:-6] + 'turf')
