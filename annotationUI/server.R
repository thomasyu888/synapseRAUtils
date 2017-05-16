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
      dat <- dat[which(dat$category %in% input$cat),]
    }
    else{
      dat
    }
    
    inFile <- input$userAnnot
    
    if (is.null(inFile))
      return(dat)
    
    # use fread to catch user defined formats and execute correct errors as needed
    user.dat <-  fread(inFile$datapath)
    # this line needs to be removed
    colnames(user.dat) <- c("key", "description", "columnType", "maximumSize", "value", "values_description", "values_source", "category")
    # user.dat <- read.csv(inFile$datapath, header = input$header, sep = input$sep, quote = input$quote)
    dat <- rbind(dat, user.dat)
    dat 
  })

  output$annotationTable <- shiny::renderDataTable({
    
    dataOut() 
  
  },options = list(lengthMenu = c(10, 50, 100), pageLength = 10))

  output$category <- renderText({
    if (is.null(input$cat)) {
      return()
    }
    if (input$cat > 0) {
      input$cat
    }
  })
  
  output$downloadSchema <- downloadHandler(
    filename <- function() {'annotations_manifest.xlsx'},
    content <- function(file) {
      
      user.dat <- dataOut()
      
      first.cols <- c("synapseId", "fileName")
      user.cols <- unique(user.dat[["key"]])
      
      columns <- append(c("synapseId", "fileName"), user.cols)
      schema <- data.frame(matrix(ncol = length(columns), nrow = 0))
      colnames(schema) <- columns
      key.description <- user.dat[,c("key", "description", "columnType", "category")]
      value.description <- user.dat[,c("key", "value", "values_description", "values_source", "category")]
      
      sheets <- list(manifest = schema , key.description = key.description, keyvalue.description = value.description)
      openxlsx::write.xlsx(sheets, file)
    
      # write.csv(schema, file, row.names = F)
      # write.csv(key.description, "key_description.csv", row.names = F)
      # write.csv(keyvalue.description, "value_description.csv", row.names = F)
    }
  )
}