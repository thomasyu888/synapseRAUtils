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
usePackage("dplyr")
usePackage("openxlsx")
usePackage("shiny")
usePackage("ggplot2")
usePackage("shinydashboard")
usePackage("data.table")


library(dplyr)
library(shiny)
library(ggplot2)
library(shinydashboard)
library(openxlsx)
library(data.table)
# source('http://depot.sagebase.org/CRAN.R')
# pkgInstall("synapseClient")
# library(synapseClient)

# ----------------------------------------------------------------------
# login to synapse
# ----------------------------------------------------------------------
# synapseLogin()

# ----------------------------------------------------------------------
options(stringsAsFactors = FALSE)
dat <- read.csv(file = "annotations/all.csv", header = T, sep = ",")
categories <- lapply(unique(dat$project), function(x) {x})
all.vars <- names(dat)
names(dat) <- c("key", "description", "columnType", "maximumSize", "value", "values_description", "values_source", "category")

# variable types ----------------------
var.class <- sapply(dat, class)

# seperate data types -----------------
categorical.vars <- names(var.class[var.class == "factor"])
numeric.vars <- names(var.class[var.class %in% c("numeric", "integer")])
