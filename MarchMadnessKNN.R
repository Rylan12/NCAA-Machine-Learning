## K Nearest Neighbors Code for Predicting Upsets ##
## By Matthew Osborne and Kevin Nowland           ##
## Note: You need to insert your datafile loc.s   ##
####################################################
library(class)


# Read in the NCAA2001_2017 data file
PastData <- read.csv("/Users/rylanpolster/PycharmProjects/NCAA-Machine-Learning/NCAA2001_2017.csv")



### Calculate the Statistics We Will be using as predictors ###

# First take subset of data that we will be using
ModelData <- PastData[,c("year","SeedType","Upset","TopSeed","TopTravel","TopGames","TopPTs","TopOppPTS","TopTOV","TopTOPer","TopSOS","BotSeed","BotTravel","BotGames","BotPTs","BotOppPTS","BotTOV","BotTOPer","BotSOS")]

# We need to eliminate entries with missing data
ModelData <- ModelData[ModelData$BotTOPer>0,]
ModelData <- ModelData[ModelData$TopTOPer>0,]

# Calculate the point differential for the teams
ModelData$TopPTDiff<-ModelData$TopPTs-ModelData$TopOppPTS
ModelData$BotPTDiff<-ModelData$BotPTs-ModelData$BotOppPTS



### We will be using k nearest neighbors to predict Upsets ###

# Set Up Test and training Data, we're using 2017 as a test set
train <- 1:511 

train.Predictors <- ModelData[train,c("TopTravel","TopPTDiff","TopTOPer","TopSOS","BotPTDiff","BotTravel","BotTOPer","BotSOS")]
train.Outcome <- ModelData[train,c("Upset")]

test.Predictors <- ModelData[-train,c("TopTravel","TopPTDiff","TopTOPer","TopSOS","BotPTDiff","BotTravel","BotTOPer","BotSOS")]
test.ActualOutcome <- ModelData[-train,c("Upset")]

# We need to standardize the values so that large variables aren't weighed more heavily

Standard.train.Pred <- scale(train.Predictors)

Standard.test.Pred <- scale(test.Predictors)

# We use 11 neighbors
knn.pred<-knn(Standard.train.Pred,Standard.test.Pred,train.Outcome,k=11)

# Calculate the error-rate for the test year 2017, this is output to the console
print(paste("The algorithm failed to correctly predict ",toString(sum(knn.pred!=test.ActualOutcome)/32*100),"% of the 2017 first round games."))

### Now we will predict for the 2018 games ###

# Load in the data from 2018
EightTeenData <- read.csv("/Users/rylanpolster/PycharmProjects/NCAA-Machine-Learning/NCAA2018.csv")

# Set Up The Data
Model18Data <- EightTeenData[,c("SeedType","TopSeed","TopTravel","TopGames","TopPTs","TopOppPTS","TopTOV","TopTOPer","TopSOS","BotSeed","BotTravel","BotGames","BotPTs","BotOppPTS","BotTOV","BotTOPer","BotSOS")]

# We need to eliminate entries with missing data
Model18Data <- Model18Data[Model18Data$BotTOPer>0,]
Model18Data <- Model18Data[Model18Data$TopTOPer>0,]

# Calculate the point differential for the teams
Model18Data$TopPTDiff <- Model18Data$TopPTs-Model18Data$TopOppPTS
Model18Data$BotPTDiff <- Model18Data$BotPTs-Model18Data$BotOppPTS

EightTeen.Predictors <- Model18Data[-train,c("TopTravel","TopPTDiff","TopTOPer","TopSOS","BotPTDiff","BotTravel","BotTOPer","BotSOS")]

# Standardize the data
Standard.18.Pred <- scale(EightTeen.Predictors)

# Get the upset predictions, outputs are 0s and 1s
knn.18.pred <- knn(Standard.train.Pred,Standard.18.Pred,train.Outcome,k=11)
UpsetPredictions <- Model18Data[,c("SeedType","TopSeed","BotSeed")]
UpsetPredictions$Prediction<-knn.18.pred
print("Reached Point")
UpsetPredictions
