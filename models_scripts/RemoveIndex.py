import arcpy
from arcpy import env

env.workspace = r'D:\Clark_County_2017_ImageClassification_Project\Samples_models\book_137_models\backup\book_137_sample.gdb'

fcs = arcpy.ListFeatureClasses()

for fc in fcs:
    try:
        arcpy.RemoveIndex_management(fc, 'AIND')
    except:
        print 'No AIND index with ' + fc




