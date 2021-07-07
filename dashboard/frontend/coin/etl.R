#backend etl script for cnn dashboard
library(stringr)
library(dplyr)
data <- readRDS("cnn/cnn_full.rds")
geo <- read.csv("cnn/mint_geo.csv")
geo <- geo[c("mint", "lat", "lon")]
abs_path <- "C:/Users/fredi/Desktop/Uni/Data Challanges/CN/"
data$mint <- str_trim(data$mint)
data <- merge(data, geo, all.x=T, by="mint")

#data_400bc <- read.csv2(paste0(abs_path,"timeperiod/new/","data_400bc_labels.csv"), dec = ".")
#data_200bc <- read.csv2(paste0(abs_path,"timeperiod/new/","data_200bc_labels.csv"), dec = ".")
#data_0bc <- read.csv2(paste0(abs_path,"timeperiod/new/","data_0bc_labels.csv"), dec = ".")
#data_0ad <- read.csv2(paste0(abs_path,"timeperiod/new/","data_0ad_labels.csv"), dec = ".")
#data_200ad <- read.csv2(paste0(abs_path,"timeperiod/new/","data_200ad_labels.csv"), dec = ".")

data_400bc <- read.csv(paste0(abs_path,"timeperiod/new/","data_400bc_labels.csv"))
data_200bc <- read.csv(paste0(abs_path,"timeperiod/new/","data_200bc_labels.csv"))
data_0bc <- read.csv(paste0(abs_path,"timeperiod/new/","data_0bc_labels.csv"))
data_0ad <- read.csv(paste0(abs_path,"timeperiod/new/","data_0ad_labels.csv"))
data_200ad <- read.csv(paste0(abs_path,"timeperiod/new/","data_200ad_labels.csv"))


data <- subset(data, select=-c(X.1,Unnamed..0, findsport, X))
#data_400bc <- subset(data_400bc, select=-c(Unnamed..0,Unnamed..0.1))
#data_200bc <- subset(data_200bc, select=-c(Unnamed..0))
#data_0bc <- subset(data_0bc, select=-c(Unnamed..0))
#data_0ad <- subset(data_0ad, select=-c(Unnamed..0))
#data_200ad <- subset(data_200ad, select=-c(Unnamed..0))

data_full_400bc <- merge( data_400bc, data, by="coin", all.x=T)
data_full_200bc <- merge( data_200bc, data, by="coin", all.x=T)
data_full_0bc <- merge( data_0bc, data, by="coin", all.x=T)
data_full_0ad <- merge( data_0ad, data, by="coin", all.x=T)
data_full_200ad <- merge( data_200ad, data, by="coin", all.x=T)
data_full_400bc$n <- 1:nrow(data_full_400bc)
data_full_200bc$n <- 1:nrow(data_full_200bc)
data_full_0bc$n <- 1:nrow(data_full_0bc)
data_full_0ad$n <- 1:nrow(data_full_0ad)
data_full_200ad$n <- 1:nrow(data_full_200ad)

saveRDS(data_full_400bc, file = "cnn/data_full_400bc.rds")
saveRDS(data_full_200bc, file = "cnn/data_full_200bc.rds")
saveRDS(data_full_0bc, file = "cnn/data_full_0bc.rds")
saveRDS(data_full_0ad, file = "cnn/data_full_0ad.rds")
saveRDS(data_full_200ad, file = "cnn/data_full_200ad.rds")

entitys <- read.csv2("cnn/design_data2.csv", dec= ".", encoding = "UTF-8")
entitys <- entitys[entitys$Label_Entity != "VERBS",]

entity_400bc <- entitys[entitys$id_coin %in% unique(data_400bc$coin),]
entity_400bc <- merge(entity_400bc, data_full_400bc[c("coin", "x", "y", "kmeans_label", "dbscan_label", "hierarchy_label")], all.x=T, by.x="id_coin", by.y="coin")
entity_200bc <- entitys[entitys$id_coin %in% unique(data_200bc$coin),]
entity_200bc <- merge(entity_200bc, data_full_200bc[c("coin", "x", "y", "kmeans_label", "dbscan_label", "hierarchy_label")], all.x=T, by.x="id_coin", by.y="coin")
entity_0bc <- entitys[entitys$id_coin %in% unique(data_0bc$coin),]
entity_0bc <- merge(entity_0bc, data_full_0bc[c("coin", "x", "y", "kmeans_label", "dbscan_label", "hierarchy_label")], all.x=T, by.x="id_coin", by.y="coin")
entity_0ad <- entitys[entitys$id_coin %in% unique(data_0ad$coin),]
entity_0ad <- merge(entity_0ad, data_full_0ad[c("coin", "x", "y", "kmeans_label", "dbscan_label", "hierarchy_label")], all.x=T, by.x="id_coin", by.y="coin")
entity_200ad <- entitys[entitys$id_coin %in% unique(data_200ad$coin),]
entity_200ad <- merge(entity_200ad, data_full_200ad[c("coin", "x", "y", "kmeans_label", "dbscan_label", "hierarchy_label")], all.x=T, by.x="id_coin", by.y="coin")

saveRDS(entity_400bc, file = "cnn/entity_400bc.rds")
saveRDS(entity_200bc, file = "cnn/entity_200bc.rds")
saveRDS(entity_0bc, file = "cnn/entity_0bc.rds")
saveRDS(entity_0ad, file = "cnn/entity_0ad.rds")
saveRDS(entity_200ad, file = "cnn/entity_200ad.rds")


entity_400bc <- entitys[entitys$id_coin %in% unique(data_400bc$coin),]
entity_400bc_detail <- merge(entity_400bc, data_full_400bc[c("coin", "x", "y", "startdate", "enddate")], all.x=T, by.x="id_coin", by.y="coin")
entity_200bc<- entitys[entitys$id_coin %in% unique(data_200bc$coin),]
entity_200bc_detail <- merge(entity_200bc, data_full_200bc[c("coin", "x", "y", "startdate", "enddate")], all.x=T, by.x="id_coin", by.y="coin")
entity_0bc <- entitys[entitys$id_coin %in% unique(data_0bc$coin),]
entity_0bc_detail <- merge(entity_0bc, data_full_0bc[c("coin", "x", "y", "startdate", "enddate")], all.x=T, by.x="id_coin", by.y="coin")
entity_0ad <- entitys[entitys$id_coin %in% unique(data_0ad$coin),]
entity_0ad_detail <- merge(entity_0ad, data_full_0ad[c("coin", "x", "y", "startdate", "enddate")], all.x=T, by.x="id_coin", by.y="coin")
entity_200ad <- entitys[entitys$id_coin %in% unique(data_200ad$coin),]
entity_200ad_detail <- merge(entity_200ad, data_full_200ad[c("coin", "x", "y", "startdate", "enddate")], all.x=T, by.x="id_coin", by.y="coin")

entity_400bc_detail$d_startdate <- floor(entity_400bc_detail$startdate/10)*10
entity_200bc_detail$d_startdate <- floor(entity_200bc_detail$startdate/10)*10
entity_0bc_detail$d_startdate <- floor(entity_0bc_detail$startdate/10)*10
entity_0ad_detail$d_startdate <- floor(entity_0ad_detail$startdate/10)*10
entity_200ad_detail$d_startdate <- floor(entity_200ad_detail$startdate/10)*10

entity_400bc_detail$d_enddate <- floor(entity_400bc_detail$enddate/10)*10
entity_200bc_detail$d_enddate <- floor(entity_200bc_detail$enddate/10)*10
entity_0bc_detail$d_enddate <- floor(entity_0bc_detail$enddate/10)*10
entity_0ad_detail$d_enddate <- floor(entity_0ad_detail$enddate/10)*10
entity_200ad_detail$d_enddate <- floor(entity_200ad_detail$enddate/10)*10


saveRDS(entity_400bc_detail, file = "cnn/entity_400bc_detail.rds")
saveRDS(entity_200bc_detail, file = "cnn/entity_200bc_detail.rds")
saveRDS(entity_0bc_detail, file = "cnn/entity_0bc_detail.rds")
saveRDS(entity_0ad_detail, file = "cnn/entity_0ad_detail.rds")
saveRDS(entity_200ad_detail, file = "cnn/entity_200ad_detail.rds")
