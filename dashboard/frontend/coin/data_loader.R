load_x_model <- reactive({
  bc400 <- readRDS("cnn/model_400bc_x.rds")
  bc200 <- readRDS("cnn/model_200bc_x.rds")
  bc0 <- readRDS("cnn/model_0bc_x.rds")
  ad0 <- readRDS("cnn/model_0ad_x.rds")
  ad200 <-readRDS("cnn/model_200ad_x.rds")
  data <- list()
  data$bc400 <- bc400
  data$bc200 <- bc200
  data$bc0 <- bc0
  data$ad0 <- ad0
  data$ad200 <- ad200
  data
})
load_y_model <- reactive({
  bc400 <- readRDS("cnn/model_400bc_y.rds")
  bc200 <- readRDS("cnn/model_200bc_y.rds")
  bc0 <- readRDS("cnn/model_0bc_y.rds")
  ad0 <- readRDS("cnn/model_0ad_y.rds")
  ad200 <-readRDS("cnn/model_200ad_y.rds")
  data <- list()
  data$bc400 <- bc400
  data$bc200 <- bc200
  data$bc0 <- bc0
  data$ad0 <- ad0
  data$ad200 <- ad200
  data
})

load_entity_data <- reactive({
  bc400 <- readRDS("cnn/entity_400bc.rds")
  bc200 <- readRDS("cnn/entity_200bc.rds")
  bc0 <- readRDS("cnn/entity_0bc.rds")
  ad0 <- readRDS("cnn/entity_0ad.rds")
  ad200 <-readRDS("cnn/entity_200ad.rds")
  data <- list()
  data$bc400 <- bc400
  data$bc200 <- bc200
  data$bc0 <- bc0
  data$ad0 <- ad0
  data$ad200 <- ad200
  data
})
load_entity_detail_data <- reactive({
  bc400 <- readRDS("cnn/entity_400bc_detail.rds")
  bc200 <- readRDS("cnn/entity_200bc_detail.rds")
  bc0 <- readRDS("cnn/entity_0bc_detail.rds")
  ad0 <- readRDS("cnn/entity_0ad_detail.rds")
  ad200 <-readRDS("cnn/entity_200ad_detail.rds")
  data <- list()
  data$bc400 <- bc400
  data$bc200 <- bc200
  data$bc0 <- bc0
  data$ad0 <- ad0
  data$ad200 <- ad200
  data
})

load_all_data <- reactive({
  bc400 <- readRDS("cnn/data_full_400bc.rds")
  bc200 <- readRDS("cnn/data_full_200bc.rds")
  bc0 <- readRDS("cnn/data_full_0bc.rds")
  ad0 <- readRDS("cnn/data_full_0ad.rds")
  ad200 <-readRDS("cnn/data_full_200ad.rds")
  data <- list()
  data$bc400 <- bc400
  data$bc200 <- bc200
  data$bc0 <- bc0
  data$ad0 <- ad0
  data$ad200 <- ad200
  data
})