#This script was written by Warren Kunkler in support of large scale image classification projects using the object detection machine learning
#methodologies. This script automates a random forest classifier for image classification

require(sp)
require(rgdal)
require(raster)
require(randomForest)

#set up input path directory of segmented 8 band stacks
path <- "D:/Clark_County_2017_ImageClassification_Project/segmented8_bandStack_125"


#creates file object and stores list of full path image names that are properly formated to automation
file.names <- dir(path, pattern = ".img", full.names = TRUE)

#creates list of output names for output directory in OutFile object
OutFile.names <- dir(path, pattern = ".img")

#loads an rf object that stores the random forest model to be used in this classification
rf <- readRDS("D:/Clark_County_2017_ImageClassification_Project/Samples_models/book_137_models/137_samples_models/RF_model_137_Model.rds")

#creates output path for each image, sets the seed for the statistical calculations to obtain reproducable random number generation
#simulates random object creation. This number is an arbitrary integer input
output_path <- "D:/Clark_County_2017_ImageClassification_Project/Samples_models/book_125_models/classified/"
set.seed(01234567890)



#loop through the file objects list of input files, loads each image, stores the image data into an image_class object
#changes the band names within the image_class object to a more generic naming convention. properly formats the output
#run the prediction method on each input segmented stack using the previously created random forest model
#outputs a thematic classified image
for(i in 1:length(file.names)){
  print(file.names[i])
  image <- brick(file.names[i])
  image_class <- image
  
  
  names(image_class) = c("b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8")
  
  
  OutputFile <- toString(OutFile.names[i])
  OutputComplete <- paste(output_path, OutputFile, sep="")
  
  #sets up a progress window, can overwrite output, does not remove any no data values. Sets the output type to response so we get a 
  #majority vote method for classification instead of regression method
  image_pred <- predict(image_class, rf, OutputComplete, type = "response", index = 7, progress="window", overwrite = TRUE, na_rm = TRUE)
  
}