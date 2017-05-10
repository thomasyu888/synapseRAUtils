# UI component  -----------------------------------------------
# UI component generates the HTML 
# HTML: hypertext markup language 
# •	Hypertext: Interactive text or overcoming the constrains of text. 
# •	Markup: Is marking up different sections of a page as lists, links, 
#   or even specifying its attributes or changing font size
# HTML language is written by “tags” while its content is 
# preserved inside the opening and closing tags.  
# Different web browsers (ex. Firefox, Chrome,…) read .html files and 
# display it (idea is to be consistent and similar)
#-------------------------------------------------------------
# https://rstudio.github.io/shinydashboard/structure.html
body <- dashboardBody(
  fluidRow(
      box(   checkboxGroupInput("cat", "Project Category:",
                                choiceNames = categories,
                                choiceValues = categories, 
                                selected = categories),
      verbatimTextOutput("category"),
      textOutput("txt")),
      shiny::dataTableOutput('annotationTable'),
      downloadButton('downloadData', 'Download'),
      downloadButton('downloadSchema', 'Download Manifest'),
      actionButton("uploadData", "Upload Your Projects' Annotation"),
      actionButton("appendData", "Request to append Your Projects' Annotation")
  )
)


# We'll save it in a variable `ui` so that we can preview it in the console
ui <- dashboardPage(
  dashboardHeader(title = "Annotation Utils UI"),
  dashboardSidebar(disable = TRUE),
  body
)

# ---------------------------------------------------------------------------
# ui <- fluidPage(
#   navbarPage("Annotations Utils UI"),
#   br(),
#   #titlePanel("title panel"),
#   sidebarLayout(position = "left",
#   sidebarPanel(
#     checkboxGroupInput("cat", "Project Category:",
#                         choiceNames = categories,
#                         choiceValues = categories, 
#                         selected = categories)
#   ),
#   downloadButton('downloadData', 'Download')
#   #textOutput("txt")
#   ),
#   mainPanel(shiny::dataTableOutput('annotationTable')
#             )
# )
