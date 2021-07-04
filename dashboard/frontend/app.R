library(shiny)
library(shinydashboard)
library(ggplot2)
library(plotly)
library(dplyr)
library(DT)
#library(leaflet)
library(stringr)
library(randomForest)
library(shinyjs)
library(sodium)



source("credentials.R")
box_height <- "40em"
threshold_mpg = 0.0
threshold_cyl = 0.0
source("ui.R")


server <- function(input, output, session) {
    #current <- reactiveValues(file = c(""), dataset = data.frame(), clusters = c(), count=0)
    login = FALSE
    USER <- reactiveValues(login = login)
    
    
    
    output$body <- renderUI({
        if (USER$login == TRUE ) {
            tabItems(
                # First tab content
                
                # Second tab content
                tabItem(tabName = "explorer",
                        fluidRow(column(12, box(width=12, h1("Filter"),  selectInput("dataset", "Select a dataset (timeperiod)", c("<400BC","400-200BC","200-0BC", "0-200AD", ">200AD")),
                                                selectInput("cluster_method", "Select the cluster algorithm", c("kmeans", "dbscan", "hierarchy"), selected = "dbscan"),
                                                selectInput("cluster_filter", "Select the cluster you want to filter", c("All"), selected = "All", multiple=T)))),
                        fluidRow(
                            column(12,
                                   # box(width=12,plotOutput("plot_explorer", click = "plot_click",
                                   #                         dblclick = "plot_dblclick",
                                   #                         hover = "plot_hover",
                                   #                         brush = "plot_brush"), 
                                   box(width=12,h1("Cluster analysis"), plotlyOutput("plot_explorer"),
                                       height = box_height))),
                        fluidRow(column(12, box(width=12, h2("Coin details"),
                                                textOutput("observations"),
                                                textOutput("avg_weight"),
                                                textOutput("avg_startdate"),
                                                textOutput("avg_enddate"),
                                                textOutput("avg_mindiam"),
                                                textOutput("avg_maxdiam"),
                                                textOutput("avg_denom"),
                                                textOutput("avg_material"),
                                                DT::dataTableOutput("explorer_table")))),
                        fluidRow(column(12, box(width=12, h2("Entity Top 10"), plotlyOutput("plot_entity")))),
                        fluidRow(column(12, box(width=12, h2("Entity details"), DT::dataTableOutput("entity_table")))),
                        #fluidRow(column(12, box(width=12, h2("Mint details"), leafletOutput("mint_map", ))))
                        fluidRow(column(12, box(width=12, h2("Mint Top 15"), plotlyOutput("mint_map", ))))
                ),
                tabItem(tabName = "entity",
                        fluidRow(
                            column(12, box(width=12,h1("Entity analysis"),
                                           selectInput("dataset_entity", "Select a dataset (timeperiod)", c("All", "<400BC","400-200BC","200-0BC", "0-200AD", ">200AD"), selected = "All"),
                                           sliderInput("enddate", "Select enddate timeperiod", min=0, max=100, value=c(40,60)),
                                           selectInput("entity_type", "Select entity type", c("All","Object","Person", "Plant"),selected="All" ),
                                           selectInput("entity_items", "Select entity type", c("All"), selected=c("All") , multiple = T)
                            ))),
                        fluidRow(
                            column(12, box(width=12,h1("Entity analysis"), plotlyOutput("plot_entity_explorer"),
                                           height = box_height))),
                        fluidRow(
                            column(12, box(width=12,h1("Entity development"), plotlyOutput("plot_entity_timeseries"),
                                           height = box_height)))),
                
                tabItem(tabName = "finder",
                        fluidRow(
                            column(12, box(width=12, h1("Select timeperiod"),selectInput("dataset_finder", "Select a dataset", c( "<400BC","400-200BC","200-0BC", "0-200AD", ">200AD"), selected = "<400BC")))),
                        fluidRow(column(12,box(width=12, h1("Select feature"),
                                               numericInput("weight", "Specify weight", 0),
                                               numericInput("startdate", "Specify startdate", 0),
                                               numericInput("enddate_finder", "Specify enddate", 0),
                                               selectInput("mint", label="Specify mint", choices=c("")),
                                               selectInput("denom", label="Specify denom", choices=c("")),
                                               selectInput("material", label="Specify material", choices=c()),
                                               actionButton("calculate", label="Calculate", width=100)
                        ))),
                        fluidRow(column(12, box(width=12, h1("Results"), DT::dataTableOutput("result_table")))),
                        fluidRow(column(12, box(width=12, h1("Entity Results"), DT::dataTableOutput("result_entity_table"))))
                        
                        
                ),
                tabItem(tabName = "help", fluidRow(column(12, box(width=12, h1("How to use this dashboard?"),
                                                                  p("The key element of this dashboard is the UMAP cluster analysis. Therefore we used the UMAP dimension reduction to plot multidimensional features of coins in a 2D plot. For the transformation we used the features weight, enddate, startdate, mint, material and denom. We filtered the data based on different timeperiods and created data subsets. All plots (without bar charts) are interactive, so please play around :-)."),
                                                                  h2("COIN EXPLORER:"),
                                                                  h3("How to Select Coins?"),
                                                                  p("1. Select a dataset based on time period"),
                                                                  #br(),
                                                                  p("2. Select coins  by clicking and dragging a selection box around coins of interest (default zoom) or use the selection tool(lasso or box selection). "),
                                                                  #br(),
                                                                  p("3. De-select coins: double-click in plot resets your selection to all coins in time period"),
                                                                  h3("How to explore Selected Coins?"),
                                                                  p("1. Coin Details: See number of selected coins via entries (below table)"),
                                                                  p("2. Entity Top: See 10 most frequent entities for selected coins in bar diagram. See frequency of individual entities on vertical axis or by hovering over respective bar"),
                                                                  p("3. Entity Details: Find all available descriptions of coins for obverse and reverse separately. Search for any term in the table to find coins with that specific characteristic via Search, e.g. to see coins showing a head, type 'Kopf'."),
                                                                  
                                                                  h3("How to export Selected Coins Data?"),
                                                                  p("Go to the table click on the download button. You can choose between different formats."),
                                                                  h2("ENTITY EXPLORER"),
                                                                  h3("How to Select Coins?"),
                                                                  p("1. Select a dataset based on time period"),
                                                                  p("2. Specify time period by moving sliders: this reflects final date in the range assigned to the coins"),
                                                                  p("3. Specify the entity type you are interested in by selection from the drop-down. By default all entity types are selected."),
                                                                  p("Hint: The loading of all timeperiod (datasets) take some time."),
                                                                  h3("How to explore Selected Coins?"),
                                                                  p("1. Entity analysis: See 15 most frequent entities for coins in selected time period. See frequency of individual entities on vertical axis or by hovering over respective bar"),
                                                                  p("2. Entity development: See all entities in selected time period by default. Select 1 specific entities by double-click on the entity name(right next to the plot). Add entities to the selection by single-click on the entity name(right next to the plot). De-Select specific entities by single-click on a selected entity name. Select all entities by double-click on a de-selected entity name."),
                                                                  h2("COIN FINDER"),
                                                                  p("Coin finder uses Machine Learning classifier to find similar coins based on the used UMAP dimension reduction. Right now, not 100% implemented. ")
                )))))
        } else {
            loginpage
        }
        
        
        })
    
    
    output$logoutbtn <- renderUI({
        req(USER$login)
        tags$li(a(icon("fa fa-sign-out"), "Logout", 
                  href="javascript:window.location.reload(true)"),
                class = "dropdown", 
                style = "background-color: #eee !important; border: 0;
                    font-weight: bold; margin:5px; padding: 10px;")
    })
    
    observe({ 
        if (USER$login == FALSE) {
            if (!is.null(input$login)) {
                if (input$login > 0) {
                    Username <- isolate(input$userName)
                    Password <- isolate(input$passwd)
                    if(length(which(credentials$username_id==Username))==1) { 
                        pasmatch  <- credentials["passod"][which(credentials$username_id==Username),]
                        pasverify <- password_verify(pasmatch, Password)
                        if(pasverify) {
                            USER$login <- TRUE
                        } else {
                            shinyjs::toggle(id = "nomatch", anim = TRUE, time = 1, animType = "fade")
                            shinyjs::delay(3000, shinyjs::toggle(id = "nomatch", anim = TRUE, time = 1, animType = "fade"))
                        }
                    } else {
                        shinyjs::toggle(id = "nomatch", anim = TRUE, time = 1, animType = "fade")
                        shinyjs::delay(3000, shinyjs::toggle(id = "nomatch", anim = TRUE, time = 1, animType = "fade"))
                    }
                } 
            }
        }    
    })
    
    
    output$sidebarpanel <- renderUI({
        if (USER$login == TRUE ){
            sidebarMenu(
                menuItem("Coin Explorer", tabName = "explorer", icon = icon("wpexplorer")),
                menuItem("Entity Explorer", tabName = "entity", icon = icon("image")),
                menuItem("Coin finder", tabName = "finder", icon = icon("search")),
                menuItem("Help", tabName = "help", icon = icon("question"))
                
                #selectInput("cluster", "Select a cluster", c(0,1,2,3), multiple=T, selected =c(0,1,2))
            )
            
        }})
    
    
    
    
    
    
    
    table <- reactiveValues(data="", entity="")
    current <- reactiveValues(avg_weight="", std_weight="", avg_enddate="", std_enddate="", avg_startdate="", std_startdate="", observations="", avg_mindiam="", std_mindiam="", avg_maxdiam="", std_maxdiam="", avg_material="", avg_denom="", avg_material_pc="", avg_denom_pc="", cluster="dbscan", cluster_name="dbscan_label", selected_cluster="All")
    source("data_loader.R")
    
    get_models <- reactive({
        req(load_x_model())
        req(load_y_model())
        x <- load_x_model()
        y <- load_y_model()
        model <- list()
        if (req(input$dataset_finder)=="<400BC"){
            model$x <- x$bc400
            model$y <- y$bc400
        }else if (req(input$dataset_finder)=="400-200BC"){
            model$x <- x$bc200
            model$y <- y$bc200
        } else if(req(input$dataset_finder)=="200-0BC") {
            model$x <- x$bc0
            model$y <- y$bc0
        } else if(req(input$dataset_finder)=="0-200AD"){

            model$x <- x$ad0
            model$y <- y$ad0
        } else {
            model$x <- x$ad200
            model$y <- y$ad200
            
        }
        model
    }
    )
    get_cluster_entity <- reactive({
        req(load_entity_data())
        data <- load_entity_data()
        if (req(input$dataset)=="<400BC"){
            dataset <- data$bc400
        }else if (req(input$dataset)=="400-200BC"){
            dataset <- data$bc200
        } else if(req(input$dataset)=="200-0BC") {
            dataset <- data$bc0
        } else if(req(input$dataset)=="0-200AD"){
            dataset <- data$ad0
        } else {
            dataset <- data$ad200
        }
        dataset
    })
    get_cluster_entity_detail <- reactive({
        req(load_entity_detail_data())
        data <- load_entity_detail_data()
        if(req(input$dataset_entity)=="All"){
            dataset <- rbind(data$bc400,data$bc200 )
            dataset <- rbind(dataset, data$bc0)
            dataset <- rbind(dataset, data$ad0)
            dataset <- rbind(dataset,data$ad200 )
        }
        else if (req(input$dataset_entity)=="<400BC"){
            dataset <- data$bc400
        }else if (req(input$dataset_entity)=="400-200BC"){
            dataset <- data$bc200
        } else if(req(input$dataset_entity)=="200-0BC") {
            dataset <- data$bc0
        } else if(req(input$dataset_entity)=="0-200AD"){
            dataset <- data$ad0
        } else {
            dataset <- data$ad200
        }
        dataset
    })
    
    get_cluster_entity_detail_finder <- reactive({
        req(load_entity_detail_data())
        data <- load_entity_detail_data()
        if (req(input$dataset_finder)=="<400BC"){
            dataset <- data$bc400
        }else if (req(input$dataset_finder)=="400-200BC"){
            dataset <- data$bc200
        } else if(req(input$dataset_finder)=="200-0BC") {
            dataset <- data$bc0
        } else if(req(input$dataset_finder)=="0-200AD"){
            dataset <- data$ad0
        } else {
            dataset <- data$ad200
        }
        dataset
    })
    get_cluster_dataset <- reactive({
        req(load_all_data())
        data <- load_all_data()
        if (req(input$dataset)=="<400BC"){
            dataset <- data$bc400
        }else if (req(input$dataset)=="400-200BC"){
            dataset <- data$bc200
        } else if(req(input$dataset)=="200-0BC") {
            dataset <- data$bc0
        } else if(req(input$dataset)=="0-200AD"){
            dataset <- data$ad0
        } else {
            dataset <- data$ad200
        }
        
        #updateSelectInput(session, "cluster", choices=unique(dataset$label),selected=unique(dataset$label))
        dataset
        
    })
    get_cluster_dataset_finder <- reactive({
        req(load_all_data())
        data <- load_all_data()
        if (req(input$dataset_finder)=="<400BC"){
            dataset <- data$bc400
        }else if (req(input$dataset_finder)=="400-200BC"){
            dataset <- data$bc200
        } else if(req(input$dataset_finder)=="200-0BC") {
            dataset <- data$bc0
        } else if(req(input$dataset_finder)=="0-200AD"){
            dataset <- data$ad0
        } else {
            dataset <- data$ad200
        }
        
        #updateSelectInput(session, "cluster", choices=unique(dataset$label),selected=unique(dataset$label))
        dataset
        
    })
    
    filter_coins <- reactive({
        req(get_cluster_dataset())
        data <- get_cluster_dataset()
        #data <- data[data$label %in% input$cluste)r,]
        if ("All" %in% current$selected_cluster){
            return(data)
        }
        if (current$cluster=="kmeans"){
            data <- data[data$kmeans_label %in% current$selected_cluster,]
        } else if (current$cluster=="dbscan"){
            data <- data[data$dbscan_label %in% current$selected_cluster,]
        } else {
            data <- data[data$hierarchy_label %in% current$selected_cluster,]
        }
        return(data)
    })
    
    output$plot_explorer <- renderPlotly({
        req(filter_coins())
        data <- filter_coins()
        
        if(current$cluster=="dbscan"){
            color_var <- data$dbscan_label
        } else if (current$cluster=="kmeans"){
            color_var <- data$kmeans_label
        } else {
            color_var <- data$hierarchy_label
        }
        if (! "All" %in% current$selected_cluster){
            data <- data[color_var %in% current$selected_cluster,]
        }
        
    
        p <- ggplot(data, aes(x=x, y=y, color=color_var)) + geom_point(size=2)
        g <- ggplotly(p, mode = "markers", type = "scatter", source="mysource", colors="turbo")
        g <-  g %>% event_register("plotly_relayout") %>% event_register("plotly_selected")
        g
    })
    
    
    get_selected_coins <- reactive({
        event.data <- event_data("plotly_relayout", source = "mysource")
        event.selection <- event_data("plotly_selected", source="mysource")
        data <- list()

        if (!is.null(nrow(event.selection))){
            data$min_x <- min(event.selection$x)
            data$min_y <- min(event.selection$y)
            data$max_x <- max(event.selection$x)
            data$max_y <- max(event.selection$y)
            return(data)
        } else{
        data$min_x <-  as.numeric(event.data[1])
        data$max_x <- as.numeric(event.data[2])
        data$min_y <-  as.numeric(event.data[3])
        data$max_y <- as.numeric(event.data[4])
        return(data)
        }
    })

    output$explorer_table <- DT::renderDataTable(server=FALSE,{
        req(get_selected_coins())
        selected_coins <- get_selected_coins()
        req(filter_coins())
        data <- filter_coins()
        
        #rows <- nearPoints(data, input$plot_click)#, threshold = 10, maxpoints = 1)
        #event.data <- event_data("plotly_click", source = "mysource")
        #browser()
        result <- data[data$x<=selected_coins$max_x & data$x>=selected_coins$min_x & data$y<=selected_coins$max_y & data$y>=selected_coins$min_y , ]
        #result <- data
        if (nrow(result)==0){
            result <- data
        }
        result <- result[c(current$cluster_name, "coin", "maxdiam", "mindiam", "weight", "startdate", "enddate", "material", "mint", "denom")]
        DT::datatable(result,  extensions = 'Buttons', options = list(
            dom = 'Bfrtip',
            buttons = 
                list('copy', list(
                    extend = 'collection',
                    buttons = c('csv', 'excel', 'pdf'),
                    text = 'Download'
                ))))
        
        #browser()
        # if (dim(rows)[1]<1){
        #     subset(data, select=-c(x,y))
        # } else{
        #     subset(rows, select=-c(x,y))
        # }
    }
        )
    
    output$entity_table <- DT::renderDataTable(server=FALSE,{
        req(coin_explorer_get_filtered_entity_data())
        result <- coin_explorer_get_filtered_entity_data()
        result <- result[c("id_coin", "design_de", "side", "Entity")]
        DT::datatable(result,  extensions = 'Buttons', options = list(
            dom = 'Bfrtip',
            buttons = 
                list('copy', list(
                    extend = 'collection',
                    buttons = c('csv', 'excel', 'pdf'),
                    text = 'Download'
                ))))
        
        
    }
    )
    
    coin_explorer_get_filtered_data <- reactive({
        req(get_selected_coins())
        selected_coins <- get_selected_coins()
        req(filter_coins())
        data <- filter_coins()
        #browser()
        result <- data[data$x<=selected_coins$max_x & data$x>=selected_coins$min_x & data$y<=selected_coins$max_y & data$y>=selected_coins$min_y , ]
        if (nrow(result)==0){
            result <- data
        }
        if(current$cluster=="dbscan"){
            color_var <- result$dbscan_label
        } else if (current$cluster=="kmeans"){
            color_var <- result$kmeans_label
        } else {
            color_var <- result$hierarchy_label
        }
        if (! "All" %in% current$selected_cluster){
            result <- result[color_var %in% current$selected_cluster,]
        }
        result
    })
    output$mint_map <- renderPlotly({
        req(coin_explorer_get_filtered_data())
        result <- coin_explorer_get_filtered_data()
        
        agg_result <- result %>%
            group_by(mint) %>%
            summarise(n=n())
        top15_mints <- head(agg_result[order(agg_result$n, decreasing=T),],15)
        #browser()
        p <- ggplot(data=top15_mints, aes(x=reorder(mint, -n), y=n)) + geom_bar(stat="identity") + xlab("Mints")
        g <- ggplotly(p, type = "bar", source="entity_plot")
        g
    })
    # output$mint_map <- renderLeaflet({
    #     req(get_selected_coins())
    #     selected_coins <- get_selected_coins()
    #     req(filter_coins())
    #     data <- filter_coins()
    #     data <- data[c("mint", "lat", "lon", "x", "y")]
    #     if(is.null(selected_coins)) { return(NULL)}
    #     result <- data[data$x<=selected_coins$max_x & data$x>=selected_coins$min_x & data$y<=selected_coins$max_y & data$y>=selected_coins$min_y , ]
    #     mymap <- leaflet() %>% addTiles() 
    #     mymap %>% 
    #         addMarkers(data = result, lng = ~lon, lat = ~lat, label=~mint,
    #                    icon = list(
    #                        group="tools",
    #                        iconSize = c(75, 75)
    #                    ))
    #     
    # })
               
    get_aggregated_entity_detail <- reactive({
        req(get_cluster_entity_detail())
        #browser()
        data <- get_cluster_entity_detail()
        input_slider <- input$enddate
        start_filter <- input_slider[1]
        end_filter <- input_slider[2]
        #browser()
        data <- data[data$d_enddate >= start_filter & data$d_enddate <= end_filter,]
        #browser()
        if (input$entity_type!="All"){
            data <- data[data$Label_Entity==toupper(input$entity_type),]
        }
        if (! input$entity_items %in% c("All")){
            data <- data[data$Entity %in% input$entity_items,]
        }
       data
    })
    
    coin_explorer_get_filtered_entity_data <- reactive({
        
        req(get_selected_coins())
        selected_coins <- get_selected_coins()
        req(get_cluster_entity())
        data <- get_cluster_entity()
        #browser()
        if(is.null(selected_coins)) { return(NULL)}
        result <- data[data$x<=selected_coins$max_x & data$x>=selected_coins$min_x & data$y<=selected_coins$max_y & data$y>=selected_coins$min_y , ]
        if (nrow(result)==0){
            result <- data
        }
        if(current$cluster=="dbscan"){
            color_var <- result$dbscan_label
        } else if (current$cluster=="kmeans"){
            color_var <- result$kmeans_label
        } else {
            color_var <- result$hierarchy_label
        }
        if (! "All" %in% current$selected_cluster){
            result <- result[color_var %in% current$selected_cluster,]
        }
        result
    })
    output$plot_entity <- renderPlotly({
        req(coin_explorer_get_filtered_entity_data())
        result <- coin_explorer_get_filtered_entity_data()
        
        agg_result <- result %>%
            group_by(Entity) %>%
            summarise(n=n())
        top10_entity <- head(agg_result[order(agg_result$n, decreasing=T),],10)
        #browser()
        p <- ggplot(data=top10_entity, aes(x=reorder(Entity, -n), y=n)) + geom_bar(stat="identity") + xlab("Entitys")
        g <- ggplotly(p, type = "bar", source="entity_plot")
        g
    })
    
    
    output$plot_entity_explorer <- renderPlotly({
        req(get_aggregated_entity_detail())
        data <- get_aggregated_entity_detail()
        
        agg_result <- data %>%
            group_by(Entity) %>%
            summarise(n=n())
        
        
        #browser()
        top15_entity <- head(agg_result[order(agg_result$n, decreasing=T),],15)
        #browser()
        p <- ggplot(data=top15_entity, aes(x=reorder(Entity, -n), y=n)) + geom_bar(stat="identity") + xlab("Entitys")
        g <- ggplotly(p, type = "bar", source="entity_plot")
        g
    })
    
    output$plot_entity_timeseries <- renderPlotly({
        req(get_aggregated_entity_detail())
        #browser()
        data <- get_aggregated_entity_detail()
        agg_result <- data %>%
            group_by(Entity, d_enddate) %>%
            summarise(n=n())
        agg_result <- agg_result[order(agg_result$d_enddate),]
        #top15_entity <- head(agg_result[order(agg_result$n, d),],15)
        #browser()
        p <- ggplot(data=agg_result, aes(x=d_enddate, y=n)) + geom_line(aes(color = Entity, linetype = Entity)) +  geom_point(aes(color = Entity, linetype = Entity)) + xlab("Timeperiod")
        g <- ggplotly(p, type = "line", source="entity_timeseries")
        g
    })
    
    observe({
        req(get_cluster_entity_detail())
        data <- get_cluster_entity_detail()
        end_choices <- unique(data$d_enddate)
        min <- min(end_choices)
        max <- max(end_choices)
        entity_items <- str_sort(unique(data$Entity) )
        entity_items <- append(entity_items, "All", after=0)
        updateSelectInput(session, "entity_items", choices=entity_items, selected="All")
        updateSliderInput(session, "enddate", value=c(min, max), min=min, max=max, step=10 )
        #end_choices <- append(end_choices, "all", after=0)
        #updateSelectInput(session, "startdate", choices=end_choices)
        #updateSelectInput(session, "enddate", choices=end_choices)
        
    })
    
    observeEvent(input$dataset_finder,
                 {
                     req(get_cluster_dataset_finder())
                     data <-  get_cluster_dataset_finder()
                     mint <- str_sort(unique(data$mint))
                     material <- str_sort(unique(data$material))
                     denom <- str_sort(unique(data$denom))
                     updateSelectInput(session, "mint", choices=mint)
                     updateSelectInput(session, "material", choices=material)
                     updateSelectInput(session, "denom", choices=denom)
                 })
    
    observeEvent(input$calculate,{
        req(get_models())
        req(get_cluster_dataset_finder())
        req(get_cluster_entity_detail_finder)
        weight <- input$weight
        startdate <- input$startdate
        enddate <- input$enddate_finder
        material <- input$material
        mint <- input$mint
        denom <- input$denom
        data <- get_cluster_dataset_finder()
        entity <- get_cluster_entity_detail_finder()
        data2 <- data
        data <- data[c("weight", "startdate", "enddate", "mint", "denom", "material")]
        new_data <- data.frame(weight, startdate, enddate, mint, denom, material)
        names(new_data) <- c("weight", "startdate", "enddate", "mint", "denom", "material")
        data <- rbind(data, new_data)
        data$mint <- as.double(as.factor(data$mint))
        data$denom <- as.double(as.factor(data$denom))
        data$material <- as.double(as.factor(data$material))
        #browser()
        model <- get_models()
        x_new <- predict(model$x, tail(data,1))
        y_new <- predict(model$y, tail(data,1))
        print(x_new)
        print(y_new)
        data2$dist <- ((data2$x-x_new)^2+(data2$y-y_new)^2)
        entity$dist <- ((entity$x-x_new)^2+(entity$y-y_new)^2)
        closest_data <- data2[data2$dist<=min(data2$dist)*1.1,]
        closest_entity <- entity[entity$dist<=min(entity$dist)*1.1,]
        closest_data <- closest_data[c("x", "y", "coin", "maxdiam", "mindiam", "weight", "startdate", "enddate", "material", "mint", "denom", "dist")]
        closest_entity <- closest_entity[c("x", "y","id_coin", "design_de", "side" ,"Entity", "dist")]
        table$data <- closest_data
        table$entity <- closest_entity
        
        
    })
    
    
    output$result_table <- DT::renderDataTable({
        if (table$data==""){ return(NULL)}
        
        DT::datatable(table$data)
    })
    
    output$result_entity_table <- DT::renderDataTable({
        if (table$entity==""){ return(NULL)}
        
        DT::datatable(table$entity)
    })
    output$observations <- renderText({ paste0("Number of observations: ",as.character(current$observations)) })
    output$avg_weight <- renderText({ paste0("Average weight: ",as.character(current$avg_weight), "  Std: ", as.character(current$std_weight)) })
    output$avg_enddate <- renderText({ paste0("Average enddate: ", as.character(current$avg_enddate), "  Std: ", as.character(current$std_enddate)) })
    output$avg_startdate <- renderText({ paste0("Average startdate: ", as.character(current$avg_startdate), "  Std: ", as.character(current$std_startdate)) })
    output$avg_mindiam <- renderText({ paste0("Average mindiam: ", as.character(current$avg_mindiam), "  Std: ", as.character(current$std_mindiam)) })
    output$avg_maxdiam <- renderText({ paste0("Average maxdiam: ", as.character(current$avg_maxdiam), "  Std: ", as.character(current$std_maxdiam)) })
    output$avg_material <- renderText({ paste0("Top material: ", as.character(current$avg_material), " ", as.character(current$avg_material_pc), " %") })
    output$avg_denom <- renderText({ paste0("Top denom: ", as.character(current$avg_denom), " ", as.character(current$avg_denom_pc), " %") })
    observe({
        req(get_selected_coins())
        selected_coins <- get_selected_coins()
        req(filter_coins())
        data <- filter_coins()
        
        #rows <- nearPoints(data, input$plot_click)#, threshold = 10, maxpoints = 1)
        #event.data <- event_data("plotly_click", source = "mysource")
        #browser()
        result <- data[data$x<=selected_coins$max_x & data$x>=selected_coins$min_x & data$y<=selected_coins$max_y & data$y>=selected_coins$min_y , ]
        #result <- data
        if (nrow(result)==0){
            result <- data
        }
        current$avg_weight <- round(mean(as.numeric(result$weight), na.rm=T),2)
        current$std_weight <- round(sd(as.numeric(result$weight), na.rm=T),2)
        current$avg_enddate <- round(mean(as.numeric(result$enddate), na.rm=T),2)
        current$std_enddate <- round(sd(as.numeric(result$enddate), na.rm=T),2)
        current$avg_startdate <- round(mean(as.numeric(result$startdate), na.rm=T),2)
        current$std_startdate <- round(sd(as.numeric(result$startdate), na.rm=T),2)
        current$observations <- nrow(result)
        current$avg_mindiam <- round(mean(as.numeric(result$mindiam), na.rm=T),2)
        current$std_mindiam <- round(sd(as.numeric(result$mindiam), na.rm=T),2)
        current$avg_maxdiam <- round(mean(as.numeric(result$maxdiam), na.rm=T),2)
        current$std_maxdiam <- round(sd(as.numeric(result$maxdiam), na.rm=T),2)
        current$avg_material <- names(sort(table(result$material),decreasing=TRUE)[1])
        current$avg_material_pc <- round((as.numeric(sort(table(result$material),decreasing=TRUE)[1]) / nrow(result))*100,2)
        current$avg_denom <- names(sort(table(result$denom),decreasing=TRUE)[1])
        current$avg_denom_pc <- round((as.numeric(sort(table(result$material),decreasing=TRUE)[1]) / nrow(result))*100,2)
        
        
        
        
    })
    
    observeEvent(input$cluster_method,{
    #observe({ 
       current$cluster <- input$cluster_method
        current$cluster_name <- paste0(input$cluster_method, "_label")
        
        
        
        data <- filter_coins()
        if(current$cluster=="dbscan"){
            color_var <- data$dbscan_label
        } else if (current$cluster=="kmeans"){
            color_var <- data$kmeans_label
        } else {
            color_var <- data$hierarchy_label
        }
        selection <- append(c("All"), unique(color_var))
        updateSelectInput(session, "cluster_filter", choices=selection, selected = "All")
        
        #r_ggplot$plot_explorer <- ggplot(data, aes(x=x, y=y, color=color_var)) + geom_point(size=2)
        
    })
    
    observeEvent(input$cluster_filter,{
        cluster_method <-  current$cluster
        current$selected_cluster <- input$cluster_filter
    }
    )
    
}

    
    

shinyApp(ui, server)