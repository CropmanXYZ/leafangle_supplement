################################################################################
# Combine Penalties for curated Multiple QTL Mapping in R\qtl                  #
# Written by Sandra Truong  10/15/2014                                         #
################################################################################
# takes in arguement --args
args <- commandArgs(TRUE)

# where permutations can be found
operm_scantwo_filepath <- args[1]
input_file_directory <- file.path(operm_scantwo_filepath)
# where combined permutations will be placed
combine_scantwo_perms_filepath <- args[2]
# where to output combined permutations
output_file_directory <- file.path(combine_scantwo_perms_filepath)

# signficance value to calculate penalities
alpha_value = 0.05

# Direct path to R libraries in wsgi-hpc
# install R libraries 
# > install.packages("qtl", lib=c("/data/thkhavi/r_lib")
.libPaths("/data/thkhavi/r_lib")

# load R/qtl library
library(qtl)

# combine permutations
setwd(output_file_directory)
files <- list.files(path=input_file_directory)

operm_1 <- paste(input_file_directory, files[1], sep="/")
operm_scantwo_combined <- readRDS(operm_1)

for (i in (2:length(files))){
  operm_iter <- paste(input_file_directory, files[i], sep="/")
  operm_scantwo_combined <- c(operm_scantwo_combined, readRDS(operm_iter))
}

# save operm_scantwo_combined
operm_scantwo_combined_name <- paste("operm_scantwo_combined", "RDS", sep=".")
saveRDS(operm_scantwo_combined, file = operm_scantwo_combined_name)

# calculate penalities for multiple QTL model traversal
penalties_name <- paste(sub("[.]","p", as.character(alpha_value)), "penalities.txt", sep="_")
sink(file = penalties_name)
print(calc.penalties(perms = operm_scantwo_combined, alpha = alpha_value))
sink()
