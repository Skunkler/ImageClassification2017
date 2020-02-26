#This script was written by Warren Kunkler in support of image classification projects
#using machine learning and object detection methodologies. This script takes the co-occurrence
#8 band stack and input raster fls segments. The outputs are segmented bands for each of the 8 individual bands
#of the 8 band stack


import arcpy, os, string, sys, time, shutil
from arcpy import env


env.overwriteOutput = True

rasters = arcpy.ListRasters()


arcpy.CheckOutExtension("Spatial")

#set up input directories and output directories
rastersegs = r'D:\Clark_County_2017_ImageClassification_Project\processing\fls'
rasterseg_move_dir = r'S:\LV_Valley_Imagery\2017\Veg_analysis\FLS_segments'

Eight_band_stacks = r'D:\Clark_County_2017_ImageClassification_Project\processing\Eight_band_stack'
Eight_move_dir = r'S:\LV_Valley_Imagery\2017\Veg_analysis\Eight_band_stack'


output_seg_shp = r'D:\Clark_County_2017_ImageClassification_Project\processing\seg_shp'
output_seg_img = r'D:\Clark_County_2017_ImageClassification_Project\processing\segmented_imagery'



#this function takes the segmented features, the output name for each file, the eight band image, and the output path of the output segment path
#this calculates and writes to disk the individual segmented bands for the co-occurrence eight band stack  
def ZonalStatsBandAct(feature, out_name, Eight_band_img, output_Seg_path):
    i = 1
    
    output_segmented_imagery = output_Seg_path + '\\Band_'
  

    
    
    try:
        for i in range(1, 9):
           
            arcpy.gp.ZonalStatistics_sa(feature, "Id", Eight_band_img + "\\Band_" + str(i), output_segmented_imagery + str(i) + '\\' + out_name + '_' + str(i) + '.tif', "MEAN", "DATA")
    except:
        print "Not a Band"
        try:
            for i in range(1,9):
                arcpy.gp.ZonalStatistics_sa(feature, "Id", Eight_band_img + "\\Layer_" + str(i), output_segmented_imagery + str(i) + "\\" + out_name + "_" + str(i) + ".tif", "MEAN", "DATA")
        except:
            for i in range(1, 9):
                arcpy.gp.ZonalStatistics_sa(feature, "FID", Eight_band_img + "\\Band_" + str(i), output_segmented_imagery + str(i) + "\\" + out_name + '_' + str(i) + '.tif', "MEAN", "DATA")


#This function takes the input fls rasters and converts them to shapefile segments
#This returns the features, and the name of the feature minus the .shp extension in a tuple
def ConvertRasterSegsToPolys(Raster, output_segs):

    raster_shp = Raster.replace('.tif', '.shp')
    

    if not os.path.exists(output_segs):
        os.makedirs(output_segs)
    
    print "converting " + rastersegs + '\\' + Raster + " to feature class"
    dsc = arcpy.Describe(r'R:\Image_ClarkCounty\2017\ClarkCounty_Collection\122\o12204.tif')
    coord_sys = dsc.spatialReference
    try:    
        arcpy.DefineProjection_management(rastersegs + '\\' + Raster, coord_sys)
    except:
        "print don't need spatial correction"
    print Raster
    print output_segs + '\\' + raster_shp
    
    arcpy.RasterToPolygon_conversion(rastersegs + '\\' + Raster, output_segs + '\\' + raster_shp, "SIMPLIFY")
    outFeature = output_segs + '\\' + raster_shp
    return (outFeature, raster_shp.replace('.shp', ''))
     






#This function takes the fls raster segs, eight band co-occurrence stacks, and associated output directories
#executes the ConvertRasterSegsToPolys and ZonalStatsBandAct functions inside the nested forloop, removes auxiliary data
#off of local drives so to create space on the user's machine
def runFirstLoop(rastersegs, output_seg_shp, eight_band_stack_dir, output_seg_img):
    env.workspace = rastersegs
    rasters = arcpy.ListRasters()


                

    for raster in rasters:
        outFeature = ConvertRasterSegsToPolys(raster, output_seg_shp)
        print outFeature[0]
        print outFeature[1]
        env.workspace = eight_band_stack_dir
        EightRasters = arcpy.ListRasters()
        for raster2 in EightRasters:
            if outFeature[1] == raster2[:-4]:
                print raster2[:-4]
                ZonalStatsBandAct(outFeature[0], outFeature[1], raster2, output_seg_img)
                shutil.move(rastersegs + '\\' + raster, rasterseg_move_dir + '\\' + raster)
                env.workspace = rastersegs
                shutil.move(Eight_band_stacks + '\\' + raster2, Eight_move_dir + '\\' + raster2)


#the initial function address call that kicks off the processing
runFirstLoop(rastersegs, output_seg_shp, Eight_band_stacks, output_seg_img)


    
