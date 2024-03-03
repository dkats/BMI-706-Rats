#!/usr/bin/env Rscript

# Load the required library
library(pedbp)
library(jsonlite)

# Parse arguments
args <- commandArgs(trailingOnly = TRUE)
q_sbp <- as.numeric(args[1])
q_dbp <- as.numeric(args[2])
age <- as.numeric(args[3])
male <- as.numeric(args[4])
height <- as.numeric(args[5])

# Call the p_bp function
results <- p_bp(q_sbp=q_sbp, q_dbp=q_dbp, age=age, male=male, height=height)

# Output the results to stdout
cat(toJSON(results))
