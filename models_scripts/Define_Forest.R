#This script was written by Warren Kunkler in support image classification projects using Machine Learning and Object
#detection methodologies. 

#grab all required external packages and R libraries
require(sp)
require(rgdal)
require(raster)
require(randomForest)


#Grab the sample 8 band segmented imagery. Used to build the model
imagery <- brick("D:/Clark_County_2017_ImageClassification_Project/Samples_models/book_137_models/137_samples_models/mosaic_sample.img")

#Grab the shapefile samples using OGR
training_samples <- readOGR("D:/Clark_County_2017_ImageClassification_Project/Samples_models/book_137_models/137_samples_models/Book_137.shp", 'Book_137')

#extract the pixel data where the training samples intersect the sample imagery and store it in a dataframe
roi_data <- extract(imagery, training_samples, df = TRUE)

#add column to the dataframe object called "desc"
#using a factor data structure, grab the ClassName column from the shapefile stored within the training_samples variable
#define that column as our descriptive ID column to be used in the desc column of the roi_data dataframe object
roi_data$desc <- as.factor(training_samples$ClassName[roi_data$ID])

#rename the long unique names associated with the raster data stored in the roi_data dataframe object as a more generic name
#also be sure the desc column is named desc
colnames(roi_data) <- c('ID', 'b1', 'b2', 'b3', 'b4','b5', 'b6', 'b7','b8', 'desc')

#write the outputs of the roi_data dataframe object to an output csv for record keeping
write.csv(roi_data, 'D:/Clark_County_2017_ImageClassification_Project/Samples_models/book_137_models/137_samples_models/rf_model_137.csv')

#read the previously exported csvdata
intable <- read.csv('D:/Clark_County_2017_ImageClassification_Project/Samples_models/book_137_models/137_samples_models/rf_model_137.csv')

#calculate the random forest model using the desc field as the categorical field for each band column in the sample
#make sure keep.forest is set to TRUE so that the parameters and setting can be stored in an RDS file, also set importance to TRUE
#so that we can see how well the model performs in classification using the OOB error rate and confusion matrix
myrf2 <- randomForest(desc ~ b1+b2+b3+b4+b5+b6+b7+b8, data = intable, type="response", keep.forest = TRUE, importance = TRUE)

#save settings of random forest model to rds file
saveRDS(myrf2, 'D:/Clark_County_2017_ImageClassification_Project/Samples_models/book_137_models/137_samples_models/RF_model_137_Model.rds')

#print the perfomance metrics of the model
print(myrf2)

#free up the myrf2 variable from the global environment
rm(myrf2)