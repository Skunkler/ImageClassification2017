#This script was created by Warren Kunkler in support of image classification projects that use machine learning and object detection methodology.
#This script takes the recently classified and cleaned turf and tree polygons, separates the two veg types in different data sets, and combines them county parcel data

import arcpy
from arcpy import env
#points to cleaned classified vector polygons
env.workspace = r'D:\Clark_County_2017_ImageClassification_Project\Samples_models\AmendedData\RoughPolys.gdb'
env.overwriteOutput = True



#defines the output for the separated out vegetation types
TreeOutput = r'D:\Clark_County_2017_ImageClassification_Project\Samples_models\AmendedData\Tree_amen.gdb'
TurfOutput = r'D:\Clark_County_2017_ImageClassification_Project\Samples_models\AmendedData\Turf_amen.gdb'

#have parcel and parcel_aox information so we gain more tabular data about ownership and retain more complete geometry from GISDBA Parcels
parcels = r'D:\Clark_County_2017_ImageClassification_Project\ParcelData.gdb\GISDBA_Parcels'

parcels_aox = r'D:\Clark_County_2017_ImageClassification_Project\ParcelData.gdb\GISDBA_Parcels_AOX'



arcpy.MakeFeatureLayer_management(parcels_aox, 'AOX_lyr')


fcs = arcpy.ListFeatureClasses()
dsc = arcpy.Describe(parcels)
coord_sys = dsc.spatialReference

#define some scratch workspaces
ScratchOutput = r'D:\Clark_County_2017_ImageClassification_Project\Samples_models\AmendedData\Scratch.gdb'
#ScratchOutput2 = r'D:\Clark_County_2017_ImageClassification_Project\Samples_models\book_126_models\Intersect.gdb'

#arcpy.AddIndex_management('AOX_lyr', 'APN', 'AIND')



for fc in fcs:

    #grab and fields from the combination of the two parcel tables that we do not want
    dropfields = fc + "_FID_GISDBA_Parcels;" + fc + "_CALC_ACRES;" + fc + "_ASSR_ACRES;" + fc + "_TXT_ANGLE;" + fc + "_LABEL_CLASS;"\
    + fc + "_PARCELTYPE;" + fc + "_TAX_DIST;" + fc + "_SE_ANNO_CAD_DATA;" + fc + "_PARCEL;GISDBA_PARCELS_AOX_OBJECTID;GISDBA_PARCELS_AOX_APN;GISDBA_PARCELS_AOX_PARCELTYPE;GISDBA_PARCELS_AOX_TAX_DIST;GISDBA_PARCELS_AOX_CALC_ACRES;GISDBA_PARCELS_AOX_ASSR_ACRES;"\
    "GISDBA_PARCELS_AOX_TXT_ANGLE;GISDBA_PARCELS_AOX_LABEL_CLASS;GISDBA_PARCELS_AOX_TAXDIST;GISDBA_PARCELS_AOX_ETALFLAG;GISDBA_PARCELS_AOX_CAPACITY;GISDBA_PARCELS_AOX_ASSDYR;GISDBA_PARCELS_AOX_CONSTYR;GISDBA_PARCELS_AOX_DOCDATE;GISDBA_PARCELS_AOX_DOCNO;"\
    "GISDBA_PARCELS_AOX_DOCMULTI;GISDBA_PARCELS_AOX_DOCVEST;GISDBA_PARCELS_AOX_SALEPRICE;GISDBA_PARCELS_AOX_SALETYPE;GISDBA_PARCELS_AOX_SALEDATE;GISDBA_PARCELS_AOX_LANDCD1;GISDBA_PARCELS_AOX_LANDACRE1;GISDBA_PARCELS_AOX_LANDVAL1;GISDBA_PARCELS_AOX_LANDCD2;"\
    "GISDBA_PARCELS_AOX_LANDACRE2;GISDBA_PARCELS_AOX_LANDVAL2;GISDBA_PARCELS_AOX_IMPVAL;GISDBA_PARCELS_AOX_TOTVAL;GISDBA_PARCELS_AOX_EXMPTCD;GISDBA_PARCELS_AOX_EXMPTVAL;GISDBA_PARCELS_AOX_LYLANDVAL;GISDBA_PARCELS_AOX_LYIMPVAL;GISDBA_PARCELS_AOX_LYTOTAL;"\
    "GISDBA_PARCELS_AOX_LYEXMPTCD;GISDBA_PARCELS_AOX_LYEXMPTVAL;GISDBA_PARCELS_AOX_NBRHOOD;GISDBA_PARCELS_AOX_ADTYPE;GISDBA_PARCELS_AOX_ADFILE;GISDBA_PARCELS_AOX_ADPAGE;GISDBA_PARCELS_AOX_ADPART;GISDBA_PARCELS_AOX_ADBLKCD;GISDBA_PARCELS_AOX_ADBLK;"\
    "GISDBA_PARCELS_AOX_ADLOTCD;GISDBA_PARCELS_AOX_ADLOT;GISDBA_PARCELS_AOX_SECTION;GISDBA_PARCELS_AOX_TOWNSHIP;GISDBA_PARCELS_AOX_RANGE;GISDBA_PARCELS_AOX_MARKAREA;GISDBA_PARCELS_AOX_SUBNAME;GISDBA_PARCELS_AOX_LANDADJ;"\
    "GISDBA_PARCELS_AOX_STATEADJ;GISDBA_PARCELS_AOX_CALCACRES;GISDBA_PARCELS_AOX_COMMONNAME;GISDBA_PARCELS_AOX_LOTSQFT;GISDBA_PARCELS_AOX_ZONE;GISDBA_PARCELS_AOX_STATIC;GISDBA_PARCELS_AOX_PARCELADDRESS;GISDBA_PARCELS_AOX_Shape_Length;GISDBA_PARCELS_AOX_Shape_Area"

    #correct the projection of the fc if it needs it, delete any small polygons
    print "making adjustments to " + fc 
    arcpy.DefineProjection_management(fc, coord_sys)
    arcpy.MakeFeatureLayer_management(fc, 'lyr')
    
    arcpy.SelectLayerByAttribute_management('lyr', 'NEW_SELECTION', 'Shape_Area <= 1')
    arcpy.DeleteFeatures_management('lyr')
    

    #intersect the classified polygon with the parcel data
    print "intersecting " + fc + " with parcels"
    try:
        arcpy.Intersect_analysis(['lyr', parcels], ScratchOutput + '\\' + fc)
        arcpy.MakeFeatureLayer_management(ScratchOutput + '\\' + fc, 'lyr2')

        arcpy.AddIndex_management('lyr2', 'APN', 'FCAIND')
    #join the fc that now has the GISDBA info and join it with ownership data, export only the non null data to second scratch gdb
        print "adding final join data to " + fc
        arcpy.AddJoin_management('lyr2', 'APN', 'AOX_lyr', 'APN')
        arcpy.SelectLayerByAttribute_management('lyr2', 'NEW_SELECTION', '{}.APN'.format(fc) + ' IS NOT NULL')
        arcpy.FeatureClassToFeatureClass_conversion('lyr2', ScratchOutput, fc + '_Int')


    #delete any unnecessary fields from the fc in the ScratchOutput2 gdb
        arcpy.DeleteField_management(ScratchOutput + '\\' + fc + '_Int', dropfields)


    #split up the turf and tree from the second scratch gdb and place them into separate gdbs based on veg type
        arcpy.MakeFeatureLayer_management(ScratchOutput + '\\' + fc + '_Int', 'lyr3')
        arcpy.SelectLayerByAttribute_management('lyr3', 'NEW_SELECTION', fc + "_gridcode = 3")
        arcpy.CopyFeatures_management("lyr3", TreeOutput + '\\' + fc + "_trees")
        arcpy.SelectLayerByAttribute_management("lyr3", "NEW_SELECTION", fc + "_gridcode = 4")
        arcpy.CopyFeatures_management("lyr3", TurfOutput + '\\' + fc + "_turf")    

    #arcpy.RemoveIndex_management('lyr2', 'FCAIND') 
    except:
        print 'Error with ' + fc


#arcpy.RemoveIndex_management('AOX_lyr', 'AIND')
