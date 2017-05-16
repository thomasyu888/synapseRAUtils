# ------------------------------------------------------------------------------
# Simple Shiny template for annotations utils 
# search, display, merge, and download prototype 
# ------------------------------------------------------------------------------
usePackage <- function(p) 
{
  if (!is.element(p, installed.packages()[,1]))
    install.packages(p, dep = TRUE)
  require(p, character.only = TRUE)
}
usePackage("jsonlite")
usePackage("tidyjson")
usePackage("dplyr")
usePackage("RCurl")
#usePackage("DT")

library(tidyjson)
library(dplyr)
library(jsonlite)
library(RCurl)
library(shiny)
library(ggplot2)
library(shinydashboard)
#library(DT)

# library(plotly)
# library(colorspace)
# library(d3heatmap)
# library(httr)
# install.packages("rjson")
# library(rjson)

# source('http://depot.sagebase.org/CRAN.R')
# pkgInstall("synapseClient")

library(synapseClient)
# ----------------------------------------------------------------------
# login to synapse
# ----------------------------------------------------------------------
synapseLogin()

# ----------------------------------------------------------------------
options(stringsAsFactors = FALSE)
dat <- read.csv(file = "annotations/all.csv", header = T, sep = ",")
# ----------------------------------------------------------------------
# read data from synapse table 
# ----------------------------------------------------------------------
# test = read.delim(getFileLocation(synGet("syn9817606")), header = TRUE)
# queryResult <- synTableQuery('select * from syn9817606')
# table <- synGet('syn9817606')



# ------------------------------------------------------------------------------
# Global variables and data matrices
# ------------------------------------------------------------------------------
# helpful links: 
# https://cran.r-project.org/web/packages/tidyjson/vignettes/introduction-to-tidyjson.html

# Download raw jason data from github repo 
# It uses libcurl under the hood to perform the request and retrieve the response.
# json.file <- getURL("https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/common/minimal_Sage_standard.json")
# json.file <- getURL("https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/common/minimal_Sage_analysis.json")
# 
# # path <- '/Users/nasim/Documents/sage-internship/sage-projects/synapseAnnotations/synapseAnnotations/data/common/minimal_Sage_standard.json'
# # min.st.data <- jsonlite::fromJSON(path, flatten = T, simplifyMatrix = T, simplifyDataFrame = T)
# 
# # json.file <- getURL("https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/common/minimal_Sage_analysis.json")
# # min.data <- jsonlite::fromJSON(json.file, flatten = T, simplifyMatrix = T, simplifyDataFrame = T)
# 
# # Read json data into an R object matrix (nested dataframe)
# min.st.json <- jsonlite::fromJSON(json.file, simplifyDataFrame = T)
# min.st.json$enumValues <- lapply(min.st.json$enumValues, function(x){
#   if (dim(x)[2] == 0) {
#     x <- data.frame(value = character(),
#                     description = character(),
#                     source = character())
#     #matrix(ncol = 3, nrow = dim(x)[1]))
#     #names(x) <- c("value", "description", "source")
#     x[1, ] <- c("", "","")
#   }
# 
#   return(x)
# })
# lapply(min.st.data$enumValues,function(x){names(x)})

# Display the internal structure of the R object
# str(min.st.json)
# dim(min.st.json)
# min.st.json[[1]] %>% head
# min.st.json[[5]] %>% as.character %>% as.tbl_json %>% json_types

# value <- lapply(min.st.json$enumValues, `[[`, "value")
# description <- lapply(min.st.json$enumValues, `[[`, "description")
# source <- lapply(min.st.json$enumValues, `[[`, "source")

# min.st.items <- min.st.json %>%
#   gather_array %>%
#   spread_values(name = jstring("name")) %>%  gather_array %>%
#   spread_values(description = jstring("description")) %>% gather_array %>%
#   spread_values(columnType = jstring("columnType")) %>%  gather_array %>%
#   spread_values(maximumSize = jnumber("maximumSize")) %>% gather_array %>%
#   enter_object("enumValues") %>% gather_array %>%
#   spread_values(
#     enumValues.value = jstring("value"),
#     enumValues.description = jstring("description"),
#     enumValues.source = jstring("source")
#   ) %>%
# select(name, description, columnType, maximumSize, enumValues.value, enumValues.description, enumValues.source)

# --------------
# error in file 
# Error in eval(expr, envir, enclos) : 
#  argument "json.column" is missing, with no default
# --------------

# --------------
# read in premade data for demo
# --------------
# standard <- read.csv(file = "standard.csv", header = T, sep = ",")
# analysis <- read.csv(file = "analysis.csv", header = T, sep = ",")
# testcat <- read.csv(file = "testcat.csv", header = T, sep = ",")

# dat <- rbind(rbind(standard, analysis), testcat)
# dat <- cbind(standard$name, standard$description, standard$columnType, standard$enumValues__value, standard$enumValues__source, standard$category)
# dat$maximumSize <- as.numeric(dat$maximumSize)
# write.csv(dat, file = "both.csv", row.names = F)
# dat <- read.csv("both.csv") 
# dat <- as.data.frame(dat, stringsAsFactor = F)
categories <- lapply(unique(dat$project), function(x) {x})
# dat <- purch_items
all.vars <- names(dat)

# variable types ----------------------
var.class <- sapply(dat, class)

# seperate data types -----------------
categorical.vars <- names(var.class[var.class == "factor"])
numeric.vars <- names(var.class[var.class %in% c("numeric", "integer")])

# --------------
# example code 
# --------------
# 
# purch_json <- '
# [
#   {
#   "name": "bob",
#   "purchases": [
#   {
#   "date": "2014/09/13",
#   "items": [
#   {"name": "shoes", "price": 187},
#   {"name": "belt", "price": 35}
#   ]
#   }
#   ]
#   },
#   {
#   "name": "susan",
#   "purchases": [
#   {
#   "date": "2014/10/01",
#   "items": [
#   {"name": "True", "price": 58},
#   {"name": "bag", "price": 118}
#   ]
#   },
#   {
#   "date": "2015/01/03",
#   "items": [
#   {"name": "shoes", "price": 115}
#   ]
#   }
#   ]
#   }
#   ]'
# purch_df <- jsonlite::fromJSON(purch_json, simplifyDataFrame = TRUE)
# purch_items <- purch_json %>%
#    gather_array %>%                                     # stack the users
#    spread_values(person = jstring("name")) %>%          # extract the user name
#    enter_object("purchases") %>% gather_array %>%       # stack the purchases
#    spread_values(purchase.date = jstring("date")) %>%   # extract the purchase date
#    enter_object("items") %>% gather_array %>%           # stack the items
#    spread_values(                                       # extract item name and price
#      item.name = jstring("name"),
#      item.price = jnumber("price")
#    ) %>%
#  select(person, purchase.date, item.name, item.price) # select only what is needed

# dat <- purch_items