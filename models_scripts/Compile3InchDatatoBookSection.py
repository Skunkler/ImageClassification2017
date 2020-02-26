#This script was written by Warren Kunkler in support of the Clark County Image Classification Project
#This script takes the quarter-quarter turf tiles and compiles them onto the book and section.

import arcpy
from arcpy import env


#input geodatabase
scratch = raw_input("Please enter the workspace of the processed turf feature classes: ")
env.workspace = scratch
env.overwriteOutput = True

fcs = arcpy.ListFeatureClasses()


#pointing to three inch tiles
threeInchTiles = r"D:\Clark_County_2017_ImageClassification_Project\bookSecEdit\Veg_Sections_3in6in.shp"

#pointing to book and sections
BookSecs = r"D:\Clark_County_2017_ImageClassification_Project\bookSecEdit\veg_tiles.shp"

#points to the output fgdb
finalOutput = raw_input("Please enter a final output fgdb: ")


Scratch=r'D:\Clark_County_2017_ImageClassification_Project\Samples_models\AmendedData\Turf_Proc\Scratch.gdb'

fcs = arcpy.ListFeatureClasses()


#declare and initialize and empty dictionary 
dataDict = {}

#use search cursor to loop through the booksection shapefile
#declares and initializes a local variable that is an empty list inside the loop
#in the nested for loop, adds the feature class to the list variable if the root book section is within the feature class
#outside of the second for loop, add this to the dictionary using the list as the value and the booksection as the key
with arcpy.da.SearchCursor(BookSecs, "BOOKSECT") as cursor:
    for row in cursor:
        print "collecting tiles that need to be merged"
        List = []
        for fc in fcs:
            if row[0] in fc:
                List.append(fc)
        dataDict[row[0]] = List
        del List


#unpacks the dictionary, pulls the list values and merges them together based on the key value

for key, values in dataDict.iteritems():
    print "merging"
    Input = dataDict[key]
    MergeList = []
    for i in Input:
        MergeList.append(str(i))
    if len(MergeList) > 0:    
        arcpy.Merge_management(MergeList, Scratch + '\\o' + key)
    del MergeList



fcs = arcpy.ListFeatureClasses()

#GISDBA AOX
parcelsAOX = r'D:\Clark_County_2017_ImageClassification_Project\ParcelData.gdb\GISDBA_Parcels_AOX'
arcpy.MakeFeatureLayer_management(parcelsAOX, 'Parcels_AOX_LYR')

#loop through the scratch workspace, locate just the merged feature classes and clean up the fields to create the proper schema with proper field names
for fc in fcs:
    if len(fc) == 6:
        print fc
        arcpy.MakeFeatureLayer_management(fc, 'BookSec_lyr')
        arcpy.AddField_management('BookSec_lyr', 'APN', 'TEXT')
        try:
            arcpy.SelectLayerByAttribute_management('BookSec_lyr', 'NEW_SELECTION', fc + '_nw_APN IS NOT NULL')
            arcpy.CalculateField_management('BookSec_lyr', 'APN', 'getVal(!' + fc + '_nw_APN!)', 'PYTHON_9.3', "def getVal(InVal):\n  return InVal")
        except:
            print "no northwest turf " + fc
        try:
            arcpy.SelectLayerByAttribute_management('BookSec_lyr', 'NEW_SELECTION', fc + '_ne_APN IS NOT NULL')
            arcpy.CalculateField_management('BookSec_lyr', 'APN', 'getVal(!' + fc + '_ne_APN!)', 'PYTHON_9.3', "def getVal(InVal):\n  return InVal")
        except:
            print "no northeast turf in " + fc

        try:
            arcpy.SelectLayerByAttribute_management('BookSec_lyr', 'NEW_SELECTION', fc + '_se_APN IS NOT NULL')
            arcpy.CalculateField_management('BookSec_lyr', 'APN', 'getVal(!' + fc + '_se_APN!)', 'PYTHON_9.3', "def getVal(InVal):\n  return InVal")
        except:
            print "no south east turf in " + fc

        try: 
            arcpy.SelectLayerByAttribute_management('BookSec_lyr', 'NEW_SELECTION', fc + '_sw_APN IS NOT NULL')
            arcpy.CalculateField_management('BookSec_lyr', 'APN', 'getVal(!' + fc + '_sw_APN!)', 'PYTHON_9.3', "def getVal(InVal):\n  return InVal")
        except:
            print "no south west turf in " + fc

        arcpy.DeleteField_management(fc, [fc+'_nw_APN', fc + '_ne_APN', fc + '_se_APN', fc + '_sw_APN'])

        arcpy.Dissolve_management(fc, finalOutput + '\\' + fc, "APN", "SUM_SUM_FRONT_YD SUM;SUM_SUM_BACK_YD SUM;SUM_SUM_NA_YD SUM")
        arcpy.MakeFeatureLayer_management(finalOutput + '\\' + fc, 'FinalTurfLyr')

        arcpy.AddField_management('FinalTurfLyr', 'LANDUSE', 'TEXT')
        arcpy.AddJoin_management('FinalTurfLyr', 'APN', 'Parcels_AOX_LYR', 'APN')
        arcpy.CalculateField_management('FinalTurfLyr', 'LANDUSE', 'getVal(!GISDBA_Parcels_AOX.LANDUSE!)', 'PYTHON_9.3', 'def getVal(inVal):\n  return inVal')
        arcpy.RemoveJoin_management('FinalTurfLyr')
        arcpy.AlterField_management('FinalTurfLyr', 'SUM_SUM_SUM_FRONT_YD', 'SUM_SUM_FRONT_YD')
        arcpy.AlterField_management('FinalTurfLyr', 'SUM_SUM_SUM_BACK_YD', 'SUM_SUM_BACK_YD')
        arcpy.AlterField_management('FinalTurfLyr', 'SUM_SUM_SUM_NA_YD', 'SUM_SUM_NA_YD')


        
        
