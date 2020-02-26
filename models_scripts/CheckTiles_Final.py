import arcpy
from arcpy import env



studyAreaFc = r"D:\Clark_County_2017_ImageClassification_Project\study_area.shp"

Book = raw_input("Enter book you would like to check: ")
fgdb = raw_input("Please enter a fgdb to check: ")

arcpy.MakeFeatureLayer_management(studyAreaFc, 'StudyLyr')
arcpy.SelectLayerByAttribute_management('StudyLyr', 'NEW_SELECTION', '"BOOKSEC" LIKE \'' + Book + "%'")

TileList = []
count = 0
with arcpy.da.SearchCursor('StudyLyr', 'BOOKSEC') as cursor:
    for row in cursor:
        TileList.append('o' + row[0])
        #print
        count += 1

        
env.workspace = fgdb

fcs = arcpy.ListFeatureClasses()

for tile in TileList:
    if tile not in fcs:
        print tile + " was not found"
    elif tile in fcs:
        continue

count2 = 0
for fc in fcs:
    count2 += 1
    if fc not in TileList:
        print fc
    
print 'total in study area: ' + str(count) + '\n total in fgdb: ' + str(count2)
