import arcpy
from arcpy import env


ws = r'D:\Clark_County_2017_ImageClassification_Project\Samples_models\AmendedData\Turf_amen.gdb'
env.workspace = ws

env.overwriteOutput = True


fcs = arcpy.ListFeatureClasses()

streetCenterLines = r'D:\Clark_County_2017_ImageClassification_Project\ParcelData.gdb\SCL_STREETS'


output = r'D:\Clark_County_2017_ImageClassification_Project\Samples_models\AmendedData\Turf_Proc\Scratch.gdb'

output2 = r"D:\Clark_County_2017_ImageClassification_Project\Samples_models\AmendedData\Turf_Proc\Turf_int.gdb"


codeblock = """def getVal(inVal):
  return inVal"""



for fc in fcs:
   
    """try:
        arcpy.RemoveIndex_management('fclyr', 'AIND')
    except:
        print "no index"
    """    
    arcpy.MakeFeatureLayer_management(fc, 'fclyr', "GISDBA_Parcels_AOX_LANDUSE in ('100','110','120','130','140','150','160','170','180','185','188','195')")
    #arcpy.AddIndex_management('fclyr', fc[:-4] + 'APN', 'AIND')
    arcpy.Dissolve_management(fc, output2 + '\\' + fc, [fc[:-4] + 'APN'])
    arcpy.MakeFeatureLayer_management(output2 + '\\' + fc, 'FinalOut')
    arcpy.AddField_management('fclyr', "YARD", "TEXT", "", "", "5", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.MakeFeatureLayer_management(streetCenterLines, 'Street')

    print 'executing near'
    arcpy.Near_analysis('fclyr', "Street", "", "NO_LOCATION", "NO_ANGLE", "PLANAR")
    arcpy.AddJoin_management('fclyr', "NEAR_FID", "Street", "OBJECTID", "KEEP_COMMON")

    print 'Selecting front and back'
    arcpy.SelectLayerByAttribute_management('fclyr', "NEW_SELECTION", fc + ".GISDBA_Parcels_AOX_STRNAME = UPPER(SCL_STREETS.STRNAME) AND " + fc + ".NEAR_DIST <= 80")
    arcpy.CalculateField_management('fclyr', 'YARD', 'getFront(!YARD!)',  "PYTHON_9.3", 'def getFront(inVal):\n  return "FRONT"')

    arcpy.SelectLayerByAttribute_management('fclyr', "NEW_SELECTION", fc + ".YARD IS NULL")

    print 'print '
    arcpy.CalculateField_management('fclyr', 'YARD', 'getBack(!YARD!)', "PYTHON_9.3", 'def getBack(inVal):\n  return "BACK"' )

    arcpy.SelectLayerByAttribute_management('fclyr', "CLEAR_SELECTION")
    arcpy.RemoveJoin_management('fclyr')
    

    arcpy.SelectLayerByAttribute_management('fclyr', "NEW_SELECTION", "YARD = 'FRONT'")
    arcpy.Dissolve_management('fclyr', output + '\\' + fc + '_Front', [fc[:-4] + 'APN', 'YARD'])

    arcpy.SelectLayerByAttribute_management('fclyr', "NEW_SELECTION", "YARD = 'BACK'")
    arcpy.Dissolve_management('fclyr', output + '\\' + fc + '_Back', [fc[:-4] + 'APN', 'YARD'])


    arcpy.SelectLayerByAttribute_management('fclyr', 'CLEAR_SELECTION')
    arcpy.Select_analysis(fc, output + '\\' + fc + '_NoFYBYTurf', "YARD IS NULL")
    arcpy.Dissolve_management(output + '\\' + fc + '_NoFYBYTurf', output + '\\' + fc + '_NoFYBYTurfDis', [fc[:-4] + 'APN', 'YARD'])
    arcpy.MakeFeatureLayer_management(output + '\\' + fc + '_NoFYBYTurfDis', 'NoFYBY_Lyr')

    arcpy.SelectLayerByAttribute_management('fclyr', "CLEAR_SELECTION")

    arcpy.MakeFeatureLayer_management(output + '\\' + fc + '_Front', 'FrontLyr')
    arcpy.MakeFeatureLayer_management(output + '\\' + fc + '_Back', 'BackLyr')

    arcpy.AddField_management('frontLyr', 'FrontYard_Area', 'DOUBLE')
    arcpy.AddField_management('frontLyr', 'BackYard_Area', 'DOUBLE')
    arcpy.AddField_management('frontLyr', 'NA_Area', 'DOUBLE')
    arcpy.CalculateField_management('frontLyr', 'FrontYard_Area', 'getVal(!Shape_Area!)', 'PYTHON_9.3', codeblock)
    arcpy.AddField_management('BackLyr', 'Proc', 'SHORT')
    arcpy.AddJoin_management('BackLyr', fc[:-4] + 'APN', 'FrontLyr', fc[:-4] + 'APN')
    arcpy.SelectLayerByAttribute_management('BackLyr', 'NEW_SELECTION', fc + "_Front.Shape_Area IS NOT NULL")
    arcpy.CalculateField_management('BackLyr', fc + '_Back.Proc', 'getProc()', 'PYTHON_9.3', 'def getProc():\n  return 1')
    arcpy.SelectLayerByAttribute_management('BackLyr', 'CLEAR_SELECTION')
    arcpy.RemoveJoin_management('BackLyr')
    
    
    
    arcpy.AddJoin_management('FrontLyr', fc[:-4] + 'APN', 'BackLyr', fc[:-4] + 'APN')
    arcpy.SelectLayerByAttribute_management('FrontLyr', 'NEW_SELECTION', fc + "_Back.Proc IS NOT NULL")
    
    arcpy.CalculateField_management('FrontLyr', fc + '_Front.BackYard_Area', 'getVal(!' + fc + '_Back.Shape_Area!)', 'PYTHON_9.3', codeblock)
    arcpy.SelectLayerByAttribute_management('FrontLyr', 'CLEAR_SELECTION')
    arcpy.RemoveJoin_management('FrontLyr')
    
    arcpy.SelectLayerByAttribute_management('BackLyr', 'NEW_SELECTION', "Proc IS NULL")
    arcpy.FeatureClassToFeatureClass_conversion('BackLyr', output,  fc + '_noFYBack')
    arcpy.SelectLayerByAttribute_management('BackLyr', 'CLEAR_SELECTION')


    arcpy.MakeFeatureLayer_management(output + '\\' + fc + '_noFYBack', 'NoFYBack_Lyr')    
    arcpy.Append_management('NoFYBack_Lyr', 'FrontLyr', 'NO_TEST')
    arcpy.SelectLayerByAttribute_management('FrontLyr', 'NEW_SELECTION', 'BackYard_Area IS NULL')
    arcpy.CalculateField_management('FrontLyr', 'BackYard_Area', 'getVal(!Shape_Area!)', 'PYTHON_9.3', codeblock)
    arcpy.SelectLayerByAttribute_management('FrontLyr', 'CLEAR_SELECTION')

    
    arcpy.Append_management('NoFYBY_Lyr', 'FrontLyr', 'NO_TEST')

    arcpy.SelectLayerByAttribute_management('FrontLyr', 'NEW_SELECTION', "FrontYard_Area IS NULL AND BackYard_Area IS NULL")
    arcpy.CalculateField_management('FrontLyr', 'NA_Area', 'getVal(!Shape_Area!)', 'PYTHON_9.3', codeblock)
    arcpy.SelectLayerByAttribute_management('FrontLyr', 'CLEAR_SELECTION')

    arcpy.AddField_management('FinalOut', 'SUM_SUM_FRONT_YD', 'DOUBLE')
    arcpy.AddField_management('FinalOut', 'SUM_SUM_BACK_YD', 'DOUBLE')
    arcpy.AddField_management('FinalOut', 'SUM_SUM_NA_YD', 'DOUBLE')
    

    arcpy.AddJoin_management('FinalOut', fc[:-4] + 'APN', 'FrontLyr', fc[:-4] + 'APN')
    arcpy.CalculateField_management('FinalOut', 'SUM_SUM_FRONT_YD', 'getVal(!' + fc + '_Front.FrontYard_Area!)', 'PYTHON_9.3', codeblock)
    arcpy.CalculateField_management('FinalOut', 'SUM_SUM_BACK_YD', 'getVal(!' + fc + '_Front.BackYard_Area!)', 'PYTHON_9.3', codeblock)
    arcpy.CalculateField_management('FinalOut', 'SUM_SUM_NA_YD', 'getVal(!' + fc + '_Front.NA_Area!)', 'PYTHON_9.3', codeblock)

    arcpy.RemoveJoin_management('FinalOut')
    
    
    #arcpy.RemoveIndex_management(fc, 'AIND')      

    


