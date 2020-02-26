import arcpy
from arcpy import env


env.workspace = r'D:\Clark_County_2017_ImageClassification_Project\FinalDatasets\Book_125_Turf.gdb'
env.overwriteOutput = True

fcs = arcpy.ListFeatureClasses()

codeblock = """def getValue(inVal):
    return inVal"""


for fc in fcs:
    if len(fc) == 6:
        print "making corrections " + fc
        arcpy.MakeFeatureLayer_management(fc, 'fcLyr')
        arcpy.AddField_management('fcLyr', 'APN', 'TEXT')
        arcpy.SelectLayerByAttribute_management('fcLyr', 'NEW_SELECTION', "\""+fc + "_ne_APN\" IS NOT NULL")
        arcpy.CalculateField_management('fcLyr', 'APN', 'getValue(!' + fc + '_ne_APN!)', "PYTHON_9.3", codeblock)

        print "making selections to NW"
        arcpy.SelectLayerByAttribute_management('fcLyr', 'NEW_SELECTION', "\""+fc+"_nw_APN\" IS NOT NULL")
        arcpy.CalculateField_management('fcLyr', 'APN', 'getValue(!' + fc + '_nw_APN!)', "PYTHON_9.3", codeblock)

        print "making selections to SE"
        arcpy.SelectLayerByAttribute_management('fcLyr', 'NEW_SELECTION', "\""+fc+"_se_APN\" IS NOT NULL")
        arcpy.CalculateField_management('fcLyr', 'APN', 'getValue(!' + fc + '_se_APN!)', "PYTHON_9.3", codeblock)

        print "making selections to SW"
        arcpy.SelectLayerByAttribute_management('fcLyr', 'NEW_SELECTION', "\""+fc+"_sw_APN\" IS NOT NULL")
        arcpy.CalculateField_management('fcLyr', 'APN', 'getValue(!' + fc + '_sw_APN!)', "PYTHON_9.3", codeblock)
        arcpy.SelectLayerByAttribute_management('fcLyr', 'CLEAR_SELECTION')

        dropFields = fc + '_ne_APN;' + fc + '_se_APN;' + fc+'_nw_APN;' + fc + 'sw_APN;'
        arcpy.DeleteField_management('fcLyr', [fc + '_ne_APN', fc+'_se_APN', fc + '_sw_APN', fc + '_nw_APN'])
    else:
        arcpy.Delete_management(fc)
