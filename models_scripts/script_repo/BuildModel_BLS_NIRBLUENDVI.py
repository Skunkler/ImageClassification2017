#Script written by Warren Kunkler in support of image classification projects using machine learning and object detection methodologies.
#loops through classified image directory and resrepo to grab corresponding images and properly format their full path location for BLS input
#The output of this script is a properly formated bls file that can be used in the batch processing of the blueir_ndvi_model.gmdx erdas spatial model

import os

#points to directory of classified imagery
input1 = r'D:\Clark_County_2017_ImageClassification_Project\Samples_models\book_126_models\classified_imagery'

#points to resrepo directory
resrepo = r'R:\Image_ClarkCounty\2017\ClarkCounty_Collection\126'

input1List = []
input1ListDir = []
input2ListDir = []

#grabs files and properly formats them

for root, dirs, files in os.walk(input1):
    for filename in files:
        if filename[-4:] == '.tif':
            input1List.append(filename[:-6] + '.tif')
            line = root + '/' + filename
            input1ListDir.append(line.replace('\\', '/'))



for root, dirs, files in os.walk(resrepo):
    for filename in files:
        if filename in input1List:
            line = root + '/' + filename
            input2ListDir.append(line.replace('\\', '/'))
            
blsFile = open(r'D:\Clark_County_2017_ImageClassification_Project\models_scripts\bls126_clean.bls', 'w')

blsFile.write('PortInput1\tPortInput2\n')

input1ListDir.sort()
input2ListDir.sort()


#writes bls file to disk and discards resources used in blsFile object
for i in range(0, len(input2ListDir)):
    line = '"{}"'.format(input2ListDir[i]) + '\t' + '"{}"'.format(input1ListDir[i]) + '\n'
    blsFile.write(line)
blsFile.close()
