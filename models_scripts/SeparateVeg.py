import arcpy
from arcpy import env

env.workspace = r'D:\Clark_County_2017_ImageClassification_Project\Samples_models\book_164_models\book_164_parcelInter.gdb'
env.overwriteOutput = True

TreeOutput = r'D:\Clark_County_2017_ImageClassification_Project\Samples_models\book_164_models\Tree_164.gdb'
TurfOutput = r'D:\Clark_County_2017_ImageClassification_Project\Samples_models\book_164_models\Turf_164.gdb'



fcs = arcpy.ListFeatureClasses()

for fc in fcs:
    print fc
    arcpy.MakeFeatureLayer_management(fc, "lyr")
    
    arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", fc + "_gridcode = 3")
    arcpy.CopyFeatures_management("lyr", TreeOutput + '\\' + fc + "_trees")
    arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", fc + "_gridcode = 4")
    arcpy.CopyFeatures_management("lyr", TurfOutput + '\\' + fc + "_turf")
    arcpy.SelectLayerByAttribute_management("lyr", "CLEAR_SELECTION")
    
