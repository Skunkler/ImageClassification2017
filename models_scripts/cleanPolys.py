#This script was written by Warren Kunkler in support of image classification projects that use the machine learning and object detection methodology.
#This script takes the classified polygons and further refines and cleans up the geometry as well as sorts the turf in shadow class to either be in the turf or tree and shrub class

import arcpy
from arcpy import env

env.workspace = r"D:\Clark_County_2017_ImageClassification_Project\Samples_models\AmendedData\RoughyPolys.gdb"
ws = env.workspace

env.overwriteOutput = True

fcs = arcpy.ListFeatureClasses()


#define some codeblocks to use to sort out the turf in shadow class
codeblock1 = """def switchTurf(valInput):
  return 4"""

codeblock2 = """def ShadowOne(valInput):
  return 4"""

codeblock3 = """def ShadowTwo(valInput):
  return 3"""

#loop through all classified feature classes
for fc in fcs:
    print fc
    #make selected feature and grab the turf class, delete any small features.
    arcpy.MakeFeatureLayer_management(fc, "lyr")
    arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", "gridcode = 4 AND Shape_Area <= 10")
    arcpy.DeleteFeatures_management("lyr")
    
    #select turf < 30 ft
    arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", "gridcode = 4 AND Shape_Area <= 30")
    arcpy.MakeFeatureLayer_management("lyr", "lyr_smallTurf")

    #grab just the normal turf
    arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", "gridcode = 4")

    """#grab the small turf, if it is close to Turf, keep it as a turf
    arcpy.SelectLayerByLocation_management("lyr_smallTurf", "WITHIN_A_DISTANCE", "lyr", "1", "NEW_SELECTION")
    arcpy.CalculateField_management("lyr_smallTurf", "gridcode", "switchTurf(!gridcode!)", "PYTHON_9.3", codeblock1)
    arcpy.SelectLayerByAttribute_management("lyr_smallTurf", "SWITCH_SELECTION")
    arcpy.CalculateField_management("lyr_smallTurf", "gridcode", "switchTurf(!gridcode!)", "PYTHON_9.3", codeblock3)"""
    

    arcpy.SelectLayerByAttribute_management("lyr", "CLEAR_SELECTION")
    arcpy.SelectLayerByAttribute_management("lyr_smallTurf", "CLEAR_SELECTION")
    
    #select shadow class, if it close to the turf then assign it as turf, otherwise assign it as tree and shrub
    arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", "gridcode = 2")
    arcpy.MakeFeatureLayer_management("lyr", "lyr_shadow")
    arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", "gridcode = 4")
    arcpy.SelectLayerByLocation_management("lyr_shadow", "WITHIN_A_Distance", "lyr", "1", "NEW_SELECTION")
    arcpy.CalculateField_management("lyr_shadow", "gridcode", "ShadowOne(!gridcode!)", "PYTHON_9.3", codeblock2)

    arcpy.SelectLayerByLocation_management("lyr_shadow", "WITHIN_A_Distance", "lyr", "1", "NEW_SELECTION", "INVERT")
    
    arcpy.CalculateField_management("lyr_shadow", "gridcode", "ShadowTwo(!gridcode!)", "PYTHON_9.3", codeblock3)

    

    
    
    
