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
    # if (is.null(dat))
    #   return(NULL)
    # elsew
    #   return(dat)
    if (input$cat > 0) {
      dat <- dat[which(dat$category %in% input$cat),]
    }
    else{
      dat
    }
  })

  output$annotationTable <- shiny::renderDataTable({

    dataOut() 
    # if (input$cat == 0) {
    #   dat 
    # }
    # dataOut()
  },options = list(lengthMenu = c(10, 50, 100), pageLength = 10))

  output$txt <- renderText({
    #icons <- paste(input$cat, collapse = ", ")
    #paste("choose your projects", icons)
  })

  output$category <- renderText({
    if (is.null(input$cat)) {
      return()
    }
    if (input$cat > 0) {
      input$cat
    }
  })

 
  output$downloadData <- downloadHandler(
    filename = function() {'project_annotations.csv'},
    content = function(file) {
      write.csv(dataOut(), file)
    }
  )
}