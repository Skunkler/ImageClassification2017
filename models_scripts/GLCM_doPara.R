#This script was written by Warren Kunkler in support various image classification projects
#This script takes input 4 band aerial imagery, calculates the co-occurrence metrics of mean and second moment
#and an NDVI and stacks into an 8 band stack. This also uses parallel processing to speed up
#production of the creation of the 8 band stacks


#gathered required external R libraries needed
require(raster)
require(rgdal)
require(glcm)
require(doParallel)
require(foreach)

#create a variable with a value of 5
UseCores <- 4

#using the socket method for the Windows operating system
#creating a cluster network of cores in our processor to use to parallel process
#multiple images at once
cl <- makeCluster(UseCores)
registerDoParallel(cl)

#defining our output and input paths
path <- "D:/Clark_County_2017_ImageClassification_Project/missing8BandStack"
Opath <- "D:/Clark_County_2017_ImageClassification_Project/Eight_band_stacks/"

#storing the full input path and image name into a list data structure
stack_list <- list.files(path, pattern = ".tif", full.names = T)

#defining an object that stores each output name
OutFile.names <- dir(path, pattern = ".tif")


#uses foreach loop to loop through each image in the stack_list, uses the dopar method to start different
#R sessions to process multiple images within the directory at once.
foreach(i=1:length(stack_list), .packages="raster") %dopar%{
  library(rgdal)
  library(glcm)
  
  #grabs the image file and loads the data values into a variable
  rasterFileIn <- brick(stack_list[i])
 
  #calculates the co-occurence matrix value for angular second moment with a 7 by 7 image kernel moving in
  #a left to right direction, stores value in textureVar. this calculation is performed on the NIR band
  textureVar <- glcm(rasterFileIn[[4]], window = c(7,7), shift=c(1,0), statistics = 'second_moment')
  
  
  #calculates the co-occurence matrix value for the mean moving in a left to right direction using a 
  #7 by 7 image kernel. Calculates this on the green band, stores results in textureVar2
  textureVar2 <- glcm(rasterFileIn[[2]], window = c(7,7), shift=c(1,0), statistics = 'mean')

  #calculates the co-occurence matrix value for the mean moving in a left to right direction using a 7
  #by 7 image kernel. Calculates this on the NIR band. Stores the results in textureVar3
  textureVar3 <- glcm(rasterFileIn[[4]], window = c(7,7), shift=c(1,0), statistics = 'mean')
  
  #Calculates an NDVI, stores the results in NDVI
  NDVI <- ((rasterFileIn[[4]] - rasterFileIn[[1]] )/(rasterFileIn[[4]] + rasterFileIn[[1]])  )
  
  #creates a variable called rasList, which stores a simple vector of different raster images
  #This includes the original 4 bands, the NDVI, and the co-occurence calculations
  rasList <- c(rasterFileIn, NDVI, textureVar2, textureVar3, textureVar)
  
  #stacks the images into an 8 band stack
  ImageFileOutput <- stack(rasList)
  
  #grabs each associated outfile name and stores it into the foreachloop local variabl outFile
  #formats the output filename properly
  OutFile <- toString(OutFile.names[i])
  OutputComplete <- paste(Opath, OutFile, sep="")
 
  #writes the final 8 band stack to disk in a .tif format
  writeRaster(ImageFileOutput, OutputComplete, format="GTiff", overwrite = TRUE )
  
}

#once processing is all completed, release the clusters back into the operating system
stopCluster(cl)