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
usePackage("openxlsx")
#usePackage("DT")

library(tidyjson)
library(dplyr)
library(jsonlite)
library(RCurl)
library(shiny)
library(ggplot2)
library(shinydashboard)
library(openxlsx)
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
categories <- lapply(unique(dat$project), function(x) {x})
all.vars <- names(dat)

# variable types ----------------------
var.class <- sapply(dat, class)

# seperate data types -----------------
categorical.vars <- names(var.class[var.class == "factor"])
numeric.vars <- names(var.class[var.class %in% c("numeric", "integer")])
