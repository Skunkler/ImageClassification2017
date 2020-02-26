import arcpy

from arcpy import env

env.workspace = r'D:\Clark_County_2017_ImageClassification_Project\Samples_models\AmendedData\Tree_amen.gdb'

env.overwriteOutput = True

fcs = arcpy.ListFeatureClasses()

#selection type
#"APN LIKE '______95%' OR APN LIKE '______99%'"
#o16414_se_APN NOT LIKE '______95%' AND o16414_se_APN NOT LIKE '______99%'


FinalOutput = r'D:\Clark_County_2017_ImageClassification_Project\Samples_models\AmendedData\Tree_Proc\Tree_amend_int.gdb'
Scratch = r'D:\Clark_County_2017_ImageClassification_Project\Samples_models\AmendedData\Scratch.gdb'

for fc in fcs:
    print "processing " + fc
    arcpy.RepairGeometry_management(fc)

    arcpy.MakeFeatureLayer_management(fc, 'lyr')
    arcpy.Dissolve_management('lyr', Scratch + '\\' + fc + '_dis', [fc[:-6] +'_APN'])

    arcpy.MakeFeatureLayer_management(Scratch + '\\' + fc + '_dis', 'DisLyr')

    arcpy.MultipartToSinglepart_management('DisLyr', Scratch + '\\' + fc + '_Sing')

    arcpy.MakeFeatureLayer_management(Scratch + '\\' + fc + '_Sing', 'SingLyr')

    arcpy.SelectLayerByAttribute_management('SingLyr', 'NEW_SELECTION', fc[:-6] + "_APN LIKE '______95%' OR " + fc[:-6] + "_APN LIKE '______99%'")

    arcpy.Eliminate_management('SingLyr', Scratch + '\\' + fc + '_elim')

    arcpy.MakeFeatureLayer_management(Scratch+ '\\' + fc + '_elim', 'FinalLyr')
    arcpy.Dissolve_management('FinalLyr', FinalOutput + '\\' + fc, [fc[:-6] + '_APN'])


    
    

    
