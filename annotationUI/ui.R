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
     # box(  #checkboxGroupInput("cat", "Project Category:",
            #                    choiceNames = categories,
            #                    choiceValues = categories, 
            #                    selected = categories)
      #verbatimTextOutput("category"),
      # textOutput("txt")
      # ),
      shiny::dataTableOutput('annotationTable'), 
      downloadButton('downloadSchema', 'Download Manifest')
      # downloadButton('downloadData', 'Download'),
      # actionButton("appendProject", "Upload Your Projects' Annotation")
      # actionButton("", "Request to append Your Projects' Annotation"),
  )
)

sidebar <- dashboardSidebar(
  sidebarMenu(
    #menuItem("Dashboard", tabName = "dashboard", icon = icon("dashboard")),
    #menuItem("Widgets", icon = icon("th"), tabName = "widgets",
             #badgeLabel = "new", badgeColor = "green")
    checkboxGroupInput("cat", "Project Category",
                       choiceNames = categories,
                       choiceValues = categories, 
                       selected = categories)
  ),
  sidebarMenu(
    tags$hr(),
    fileInput('userAnnot', 'Your Annotation CSV File',
              accept = c('text/csv', 
                       'text/comma-separated-values,text/plain', 
                       '.csv')),
    #tags$hr(),
    checkboxInput('header', 'Header', TRUE),
    radioButtons('sep', 'Separator',
                  c(Comma = ',',
                   Semicolon = ';',
                   Tab = '\t'), ','),
    radioButtons('quote', 'Quote',
                  c(None = '',
                    'Double Quote' = '"',
                    'Single Quote' = "'"),
                  '"')
  )
)

# We'll save it in a variable `ui` so that we can preview it in the console
y <- dashboardPage(
  dashboardHeader(title = "How-TO's"),
  dashboardSidebar(disable = TRUE),
  dashboardBody()
)

x <- dashboardPage(
  dashboardHeader(title = "Annotation Utils UI"),
  sidebar,
  body
)

ui <- shinyUI(
  x
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
