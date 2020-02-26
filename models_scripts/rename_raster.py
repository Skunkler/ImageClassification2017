import arcpy
from arcpy import env

env.workspace = r'D:\Clark_County_2017_ImageClassification_Project\book_161OtherReclass'
fcs = arcpy.ListRasters()

for fc in fcs:
    print fc
    arcpy.Rename_management(fc, fc[:-6] + '.tif')
