# 
library(caret)
library(randomForest)
library(stringr)
data_full_400bc <- readRDS("cnn/data_full_400bc.rds")

data_full_400bc["material"] <- ifelse(data_full_400bc["material"]==" av ", 6, ifelse(data_full_400bc["material"]==" ar ", 5, ifelse(data_full_400bc["material"]==" cu ", 4, ifelse(data_full_400bc["material"]==" ae ", 3, ifelse(data_full_400bc["material"]==" el ", 2, ifelse(data_full_400bc["material"]==" pb ", 1, 0))))))
data_full_200bc <- readRDS("cnn/data_full_200bc.rds")

data_full_200bc["material"] <- ifelse(data_full_200bc["material"]==" av ", 6, ifelse(data_full_200bc["material"]==" ar ", 5, ifelse(data_full_200bc["material"]==" cu ", 4, ifelse(data_full_200bc["material"]==" ae ", 3, ifelse(data_full_200bc["material"]==" el ", 2, ifelse(data_full_200bc["material"]==" pb ", 1, 0))))))

data_full_0bc <- readRDS("cnn/data_full_0bc.rds")

data_full_0bc["material"] <- ifelse(data_full_0bc["material"]==" av ", 6, ifelse(data_full_0bc["material"]==" ar ", 5, ifelse(data_full_0bc["material"]==" cu ", 4, ifelse(data_full_0bc["material"]==" ae ", 3, ifelse(data_full_0bc["material"]==" el ", 2, ifelse(data_full_0bc["material"]==" pb ", 1, 0))))))

data_full_0ad <- readRDS("cnn/data_full_0ad.rds")

data_full_0ad["material"] <- ifelse(data_full_0ad["material"]==" av ", 6, ifelse(data_full_0ad["material"]==" ar ", 5, ifelse(data_full_0ad["material"]==" cu ", 4, ifelse(data_full_0ad["material"]==" ae ", 3, ifelse(data_full_0ad["material"]==" el ", 2, ifelse(data_full_0ad["material"]==" pb ", 1, 0))))))

data_full_200ad <- readRDS("cnn/data_full_200ad.rds")

data_full_200ad["material"] <- ifelse(data_full_200ad["material"]==" av ", 6, ifelse(data_full_200ad["material"]==" ar ", 5, ifelse(data_full_200ad["material"]==" cu ", 4, ifelse(data_full_200ad["material"]==" ae ", 3, ifelse(data_full_200ad["material"]==" el ", 2, ifelse(data_full_200ad["material"]==" pb ", 1, 0))))))


# filter necessary columns
rf_method <- "cforrest"
data_full_400bc <- data_full_400bc[c("weight", "startdate", "enddate", "lon", "lat", "material", "y")]
#data_full_400bc$mint <- as.double(as.factor(data_full_400bc$mint))
#data_full_400bc$denom <- as.double(as.factor(data_full_400bc$denom))
#data_full_400bc$material <- as.double(as.factor(data_full_400bc$material))
rf_fit <- randomForest(y ~ ., 
                data = data_full_400bc, 
                )
rf_fit
saveRDS(rf_fit, "cnn/model_400bc_y.rds")

data_full_200bc <- data_full_200bc[c("weight", "startdate", "enddate", "lon", "lat", "material", "y")]
#data_full_200bc$mint <- as.double(as.factor(data_full_200bc$mint))
#data_full_200bc$denom <- as.double(as.factor(data_full_200bc$denom))
#data_full_200bc$material <- as.double(as.factor(data_full_200bc$material))
rf_fit <- randomForest(y ~ ., 
                data = data_full_200bc)
rf_fit
saveRDS(rf_fit, "cnn/model_200bc_y.rds")
data_full_0bc <- data_full_0bc[c("weight", "startdate", "enddate", "lon", "lat", "material", "y")]
#data_full_0bc$mint <- as.double(as.factor(data_full_0bc$mint))
#data_full_0bc$denom <- as.double(as.factor(data_full_0bc$denom))
#data_full_0bc$material <- as.double(as.factor(data_full_0bc$material))
rf_fit <- randomForest(y ~ ., 
                data = data_full_0bc)
rf_fit
saveRDS(rf_fit, "cnn/model_0bc_y.rds")
data_full_0ad <- data_full_0ad[c("weight", "startdate", "enddate", "lon", "lat", "material", "y")]
#data_full_0ad$mint <- as.double(as.factor(data_full_0ad$mint))
#data_full_0ad$denom <- as.double(as.factor(data_full_0ad$denom))
#data_full_0ad$material <- as.double(as.factor(data_full_0ad$material))
rf_fit <- randomForest(y ~ ., 
                data = data_full_0ad)
rf_fit
saveRDS(rf_fit, "cnn/model_0ad_y.rds")
data_full_200ad <- data_full_200ad[c("weight", "startdate", "enddate", "lon", "lat", "material", "y")]
#data_full_200ad$mint <- as.double(as.factor(data_full_200ad$mint))
#data_full_200ad$denom <- as.double(as.factor(data_full_200ad$denom))
#data_full_200ad$material <- as.double(as.factor(data_full_200ad$material))
rf_fit <- randomForest(y ~ ., 
                data = data_full_200ad)
rf_fit
saveRDS(rf_fit, "cnn/model_200ad_y.rds")



data_full_400bc <- readRDS("cnn/data_full_400bc.rds")

data_full_400bc["material"] <- ifelse(data_full_400bc["material"]==" av ", 6, ifelse(data_full_400bc["material"]==" ar ", 5, ifelse(data_full_400bc["material"]==" cu ", 4, ifelse(data_full_400bc["material"]==" ae ", 3, ifelse(data_full_400bc["material"]==" el ", 2, ifelse(data_full_400bc["material"]==" pb ", 1, 0))))))
data_full_200bc <- readRDS("cnn/data_full_200bc.rds")

data_full_200bc["material"] <- ifelse(data_full_200bc["material"]==" av ", 6, ifelse(data_full_200bc["material"]==" ar ", 5, ifelse(data_full_200bc["material"]==" cu ", 4, ifelse(data_full_200bc["material"]==" ae ", 3, ifelse(data_full_200bc["material"]==" el ", 2, ifelse(data_full_200bc["material"]==" pb ", 1, 0))))))

data_full_0bc <- readRDS("cnn/data_full_0bc.rds")

data_full_0bc["material"] <- ifelse(data_full_0bc["material"]==" av ", 6, ifelse(data_full_0bc["material"]==" ar ", 5, ifelse(data_full_0bc["material"]==" cu ", 4, ifelse(data_full_0bc["material"]==" ae ", 3, ifelse(data_full_0bc["material"]==" el ", 2, ifelse(data_full_0bc["material"]==" pb ", 1, 0))))))

data_full_0ad <- readRDS("cnn/data_full_0ad.rds")

data_full_0ad["material"] <- ifelse(data_full_0ad["material"]==" av ", 6, ifelse(data_full_0ad["material"]==" ar ", 5, ifelse(data_full_0ad["material"]==" cu ", 4, ifelse(data_full_0ad["material"]==" ae ", 3, ifelse(data_full_0ad["material"]==" el ", 2, ifelse(data_full_0ad["material"]==" pb ", 1, 0))))))

data_full_200ad <- readRDS("cnn/data_full_200ad.rds")

data_full_200ad["material"] <- ifelse(data_full_200ad["material"]==" av ", 6, ifelse(data_full_200ad["material"]==" ar ", 5, ifelse(data_full_200ad["material"]==" cu ", 4, ifelse(data_full_200ad["material"]==" ae ", 3, ifelse(data_full_200ad["material"]==" el ", 2, ifelse(data_full_200ad["material"]==" pb ", 1, 0))))))


# filter necessary columns

data_full_400bc <- data_full_400bc[c("weight", "startdate", "enddate", "lon", "lat", "material", "x")]
#data_full_400bc$mint <- as.double(as.factor(data_full_400bc$mint))
#data_full_400bc$denom <- as.double(as.factor(data_full_400bc$denom))
#data_full_400bc$material <- as.double(as.factor(data_full_400bc$material))
rf_fit <- randomForest(x ~ ., 
                data = data_full_400bc)
rf_fit
saveRDS(rf_fit, "cnn/model_400bc_x.rds")

data_full_200bc <- data_full_200bc[c("weight", "startdate", "enddate", "lon", "lat", "material", "x")]
#data_full_200bc$mint <- as.double(as.factor(data_full_200bc$mint))
#data_full_200bc$denom <- as.double(as.factor(data_full_200bc$denom))
#data_full_200bc$material <- as.double(as.factor(data_full_200bc$material))
rf_fit <- randomForest(x ~ ., 
                data = data_full_200bc)
rf_fit
saveRDS(rf_fit, "cnn/model_200bc_x.rds")
data_full_0bc <- data_full_0bc[c("weight", "startdate", "enddate", "lon", "lat", "material", "x")]
#data_full_0bc$mint <- as.double(as.factor(data_full_0bc$mint))
#data_full_0bc$denom <- as.double(as.factor(data_full_0bc$denom))
#data_full_0bc$material <- as.double(as.factor(data_full_0bc$material))
rf_fit <- randomForest(x ~ ., 
                data = data_full_0bc)
rf_fit
saveRDS(rf_fit, "cnn/model_0bc_x.rds")
data_full_0ad <- data_full_0ad[c("weight", "startdate", "enddate", "lon", "lat", "material", "x")]
#data_full_0ad$mint <- as.double(as.factor(data_full_0ad$mint))
#data_full_0ad$denom <- as.double(as.factor(data_full_0ad$denom))
#data_full_0ad$material <- as.double(as.factor(data_full_0ad$material))
rf_fit <- randomForest(x ~ ., 
                data = data_full_0ad)
rf_fit
saveRDS(rf_fit, "cnn/model_0ad_x.rds")
data_full_200ad <- data_full_200ad[c("weight", "startdate", "enddate", "lon", "lat", "material", "x")]
#data_full_200ad$mint <- as.double(as.factor(data_full_200ad$mint))
#data_full_200ad$denom <- as.double(as.factor(data_full_200ad$denom))
#data_full_200ad$material <- as.double(as.factor(data_full_200ad$material))
rf_fit <- randomForest(x ~ ., 
                data = data_full_200ad)
rf_fit
saveRDS(rf_fit, "cnn/model_200ad_x.rds")







