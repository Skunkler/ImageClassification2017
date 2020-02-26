require(raster)
require(rgdal)
require(doParallel)
require(foreach)
require(randomForest)

UserCores <- 5

cl= makeCluster(UserCores)

registerDoParallel(cl)

path <- "D:/Clark_County_2017_ImageClassification_Project/segmented_output_8bands/book_176"
Opath <- "D:/Clark_County_2017_ImageClassification_Project/Samples_models/book_176_models/classified_imagery/"

stack_list <- list.files(path, pattern = ".tif", full.names = T)

OutFile.names <- dir(path, pattern = ".tif")
rf <- readRDS("D:/Clark_County_2017_ImageClassification_Project/Samples_models/book_176_models/RF_model_176_Model.rds")

set.seed(01234567890)


foreach(i=1:length(stack_list), .packages="raster", "randomForest") %dopar%{
 library(randomForest)
  library(rgdal)
  
  rasterFileIN <- brick(stack_list[i])
  image_class <- rasterFileIN
  
  names(image_class) = c("b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8")
  
  OutputFile <- toString(OutFile.names[i])
  OutputComplete <- paste(Opath, OutputFile, sep="")
  
  image_pred <- predict(image_class, rf, OutputComplete, type = "response", index = 7, overwrite = TRUE, na_rm = TRUE)
}

stopCluster(cl)