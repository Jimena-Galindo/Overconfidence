# packages and parameters for the project
library(data.table)
library(here)
library(huxtable)
library(broom)
library(magrittr)
library(languageserver)
library(reticulate)
library(car) # for linearHypothesis
library(lmtest) # for coefTest
library(sandwich) # for clustering errors
library(stargazer) # for regression tables

# keep the packages synced with the lockfile
invisible(capture.output(renv::snapshot()))

# parameters
params <- list(date_of_exp = "2023-04-01")