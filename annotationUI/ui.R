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
      box(checkboxGroupInput("icons", "Project Category:",
                             choiceNames = lapply(unique(dat$category), function(x) {x}),
                             #list(icon("bug"), icon("calender"))
                             choiceValues = lapply(unique(dat$category), function(x) {x})),
      textOutput("txt")),
      tabPanel('category ', dataTableOutput('mytable')),
      downloadButton('downloadData', 'Download')
  )
)


# We'll save it in a variable `ui` so that we can preview it in the console
ui <- dashboardPage(
  dashboardHeader(title = "Annotation Utils UI"),
  dashboardSidebar(disable = TRUE),
  # dashboardSidebar(
  #   checkboxGroupInput("icons", "Choose Project Category:",
  #                      choiceNames = list(icon("calendar"), icon("bed"),
  #                                         icon("cog"), icon("bug")),
  #                      choiceValues = list("calendar", "bed", "cog", "bug")
  #   ), 
  #   textOutput("txt")
  # ),
  body
)

# ui <- fluidPage(
#   navbarPage("Annotations Utils UI"),
#   br(),
#   #titlePanel("title panel"),
#   sidebarLayout(position = "left",
#   sidebarPanel(
#     checkboxGroupInput("icons", "Choose icons:",
#                         choiceNames =
#                           list(icon("calendar"), icon("bed"),
#                                icon("cog"), icon("bug")),
#                         choiceValues =
#                          list("calendar", "bed", "cog", "bug")
#     ),
#     textOutput("txt")
#   ),
#   mainPanel(
#     tabPanel(
#       'category ', dataTableOutput('mytable')
#     )
#   )
#   )
# )