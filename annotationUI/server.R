#-------------------------------------------------------------
# Server function assembles input and outputs from ui object 
# and renders *in from and *out of a web page
# inputs can be toggled by user 
# outputs are information displays 
#-------------------------------------------------------------
server <- function(input, output) {
  # use the same name from output functions in ui
  # render function creates the type of output
  dataOut <- reactive({
    if (input$cat > 0) {
      dat <- dat[which(dat$project %in% input$cat),]
    }
    else{
      dat
    }
    
    inFile <- input$userAnnot
    
    if (is.null(inFile))
      return(dat)
    
    user.dat <- read.csv(inFile$datapath, header = input$header, sep = input$sep, quote = input$quote)
    dat <- rbind(dat, user.dat)
    dat 
  })

  output$annotationTable <- shiny::renderDataTable({
    
    dataOut() 
  
  },options = list(lengthMenu = c(10, 50, 100), pageLength = 10))

  #output$txt <- renderText({
    #icons <- paste(input$cat, collapse = ", ")
    #paste("choose your projects", icons)
  #})

  output$category <- renderText({
    if (is.null(input$cat)) {
      return()
    }
    if (input$cat > 0) {
      input$cat
    }
  })
  
  # output$appendProject <- downloadHandler(
  #   filename = function() {'project_annotations.csv'},
  #   content = function(file) {
  #     write.csv(dataOut(), file, row.names = F)
  #   }
  # )
  
  output$downloadSchema <- downloadHandler(
    filename <- function() {'annotations_manifest.xlsx'},
    content <- function(file) {
      
      user.dat <- dataOut()
      
      first.cols <- c("synapseId", "fileName")
      user.cols <- unique(user.dat[["name"]])
      
      columns <- append(c("synapseId", "fileName"), user.cols)
      print(columns)
      print(user.dat)
      schema <- data.frame(matrix(ncol = length(columns), nrow = 0))
      print(schema)
      colnames(schema) <- columns
      print(schema)
      key.description <- user.dat[,c("name", "description", "columnType", "project")]
      colnames(key.description) <- c("key", "description", "columnType", "category")
      value.description <- user.dat[,c("name", "enumValues_value", "enumValues_description", "enumValues_source", "project")]
      colnames(value.description) <- c("key", "value", "description", "source", "category")
      
      sheets <- list(manifest = schema , key.description = key.description, keyvalue.description = value.description)
      openxlsx::write.xlsx(sheets, file)
      # write.csv(dataOut(), file, row.names = F)
      # write.csv(schema, file, row.names = F)
      # write.csv(key.description, "key_description.csv", row.names = F)
      # write.csv(keyvalue.description, "value_description.csv", row.names = F)
    }
  )
}