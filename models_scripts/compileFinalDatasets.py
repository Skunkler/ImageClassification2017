import arcpy
from arcpy import env

env.workspace = r'S:\LV_Valley_Imagery\2017\Veg_analysis\FINAL_by_Section\Tree_sections\AccTree\Tree_Sections_FV_clip.gdb'

fcs = arcpy.ListFeatureClasses()

target_fc = 'trees_12319'

for fc in fcs:
    if fc != target_fc:
        print "appending " + fc + " to " + target_fc
        arcpy.Append_management(fc, target_fc, 'NO_TEST')
