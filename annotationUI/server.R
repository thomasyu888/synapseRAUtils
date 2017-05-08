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
    dat
  })

  output$mytable = renderDataTable({
    dataOut()
  })

  output$txt <- renderText({
    icons <- paste(input$icons, collapse = ", ")
    # paste("choose your projects", icons)
  })
}