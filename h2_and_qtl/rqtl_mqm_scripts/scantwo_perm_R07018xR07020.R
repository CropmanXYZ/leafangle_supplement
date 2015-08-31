################################################################################
# Calculate Penalties for curated Multiple QTL Mapping in R\qtl                #
# Written by Sandra Truong  10/14/2014                                         #
# Much of the code originates from http://www.rqtl.org/tutorials               #
################################################################################
# Rscript this_script.R ${SCANTWOPERMPATH} ${PERMUTATIONS_PER_JOB} ${JOBNUMBER} ${RQTLCROSSPATH} ${CROSS}
# takes in arguement --args
args <- commandArgs(TRUE)

operm_scantwo_filepath <- args[1]
setwd(file.path(operm_scantwo_filepath))

perms_per_job = args[2]

operm_scantwo_iteration <- paste(args[3], "operm_scantwo", sep="_")
operm_scantwo_name <- paste(operm_scantwo_iteration, "RDS", sep=".")

input_file_directory <- file.path(args[4])

input_file_name <- paste("./", args[5], ".csv", sep="")
input_file_name_cross <- file.path(input_file_name)

generation_interval = 5
phenotype_list=c("angle_leaf_3_avg_gh204A_2013_normalized",
                 "angle_leaf_4_avg_gh204A_2013_normalized",
                 "angle_leaf_3_avg_csfield_2014_rep1_normalized",
                 "angle_leaf_4_avg_csfield_2014_rep1_normalized",
                 "angle_leaf_5_avg_csfield_2014_rep1_normalized",
                 "angle_leaf_3_avg_csfield_2014_rep2_normalized",
                 "angle_leaf_4_avg_csfield_2014_rep2_normalized",
                 "angle_leaf_5_avg_csfield_2014_rep2_normalized")

################################################################################
# Direct path to R libraries in wsgi-hpc
# install R libraries 
# > install.packages("qtl", lib=c("/data/thkhavi/r_lib")
.libPaths("/data/thkhavi/r_lib")
# load R/qtl library
library(qtl)
# load snow library
library(snow)
################################################################################

# Read in cross
cross_inputcross <- read.cross(format="csvr", 
                               dir=input_file_directory,
			       file=input_file_name_cross, 
                     	       BC.gen=0, 
                               F.gen=generation_interval,
                               genotypes=c("AA","AB","BB","D","C"))
# If the cross type is considered a RIL keep the next line, if not comment out with "#"
# cross_inputcross <- convert2riself(cross_inputcross)

# scantwo as currently implemented (10/2014) is unable to handle > 1400 markers
# If your genetic map is made of more than 1400 markers, you may need to thin out markers:
# Choose the distance (in cM) to thin out
marker_distance = 2
# Check and drop markers, if appropriate
if (totmar(cross_inputcross) > 100)
{
	cross_inputcross_map <- pull.map(cross_inputcross) 
	markers2keep <- lapply(cross_inputcross_map, pickMarkerSubset, min.distance=marker_distance) 
	cross_sub <- pull.markers(cross_inputcross, unlist(markers2keep))
	cross_inputcross <- cross_sub
}
cross_inputcross <- calc.genoprob(cross_inputcross, map.function="haldane")
cross_inputcross <- sim.geno(cross_inputcross, map.function="haldane")

print(totmar(cross_inputcross))

# scantwo permutations
seed_number_base = 85842518
seed_number = seed_number_base + as.integer(args[3])
set.seed(seed_number)
operm_scantwo <- scantwo(cross=cross_inputcross, n.perm = as.integer(perms_per_job), pheno.col = phenotype_list, n.cluster = 8)
saveRDS(operm_scantwo, file = operm_scantwo_name)
