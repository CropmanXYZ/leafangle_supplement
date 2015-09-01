#!/bin/bash
############
# bash script to run scantwo permutations
# Written by Sandra Truong
# 10/15/2014

# cross name
CROSS="BTx623xIS3620C" 

# Hardware values
NUMTHREADS=8
MEMORY="32g"
# permutations
PERMUTATIONS=24000
PERMUTATIONS_PER_JOB=16
NUMBER_OF_JOBS=$(($PERMUTATIONS / $PERMUTATIONS_PER_JOB))
#PERMUTATIONS=16
#PERMUTATIONS_PER_JOB=8
#NUMBER_OF_JOBS=2


# file paths
RQTLCROSSPATH=/data/thkhavi/rqtl_crosses
if [ -d "${RQTLCROSSPATH}" ]
then
        echo -e "RQTLCROSSPATH exists"
else
        echo -e "\n\tUnable to locate RQTLCROSS_FILEPATH. Creating directory...\n"
fi

RQTLCROSS_FILEPATH=/data/thkhavi/rqtl_crosses/${CROSS}.csv
if [ -a "${RQTLCROSS_FILEPATH}" ]
then
        echo -e "RQTLCROSS_FILEPATH exists"
else
        echo -e "\n\tUnable to locate RQTLCROSS_FILEPATH.\n\tPlease make sure the R/qtl cross object is in the appropriate file.\n"
fi

CROSSPATH=/data/thkhavi/rqtl_mqm_output/${CROSS}/
if [ -d ${CROSSPATH} ]
then
	echo -e "CROSSPATH exists"
else
	echo -e "\n\tUnable to locate CROSSPATH. Creating directory...\n"
	mkdir ${CROSSPATH}
fi

LOGPATH=${CROSSPATH}logs/
if [ -d ${LOGPATH} ]
then
        echo -e "LOGPATH exists"
else
        echo -e "\n\tUnable to locate LOGPATH. Creating directory...\n"
        mkdir ${LOGPATH}
fi

SCANTWOPERM_R_FILEPATH=/data/thkhavi/rqtl_mqm_scripts/scantwo_perm_${CROSS}.R
SCANTWOPERM_BASH_FILEPATH=/data/thkhavi/rqtl_mqm_scripts/scantwo_perm_job.sh

SCANTWOPERMPATH=${CROSSPATH}operms_scantwo
if [ -d ${SCANTWOPERMPATH} ]
then
        echo -e "SCANTWOPERMPATH exists"
else
        echo -e "\n\tUnable to locate SCANTWOPERMPATH. Creating directory...\n"
        mkdir ${SCANTWOPERMPATH}
fi

COMBINESCANTWOPERM_R_FILEPATH=/data/thkhavi/rqtl_mqm_scripts/combine_scantwo_perms.R

COMBINESCANTWOPERMPATH=${CROSSPATH}mqm_scantwo_penalties/
if [ -d ${COMBINESCANTWOPERMPATH} ]
then
        echo -e "COMBINESCANTWOPERMPATH exists"
else
        echo -e "\n\tUnable to locate COMBINESCANTWOPERMPATH. Creating directory...\n"
        mkdir ${COMBINESCANTWOPERMPATH}
fi

# Perform scantwo permutations
for ((jobs=1 ; jobs<=NUMBER_OF_JOBS ; jobs++)) 
do 
	numJobs=`qstat | wc -l`
	jobsAllowed=70
	while [ $numJobs -ge $jobsAllowed ]
	do
		echo `date` "There are $numJobs in queue. Waiting for some jobs to finish before submitting more."
		sleep 30
		numJobs=`qstat | wc -l`
        done

	echo "$jobs"
	qsub -N scantwoperm_${CROSS}_$jobs -pe mpi ${NUMTHREADS} -q normal.q -l mem_free=${MEMORY} -o ${LOGPATH}scantwoperm_${CROSS}_$jobs.o -e ${LOGPATH}scantwoperm_${CROSS}_$jobs.e ${SCANTWOPERM_BASH_FILEPATH} ${SCANTWOPERM_R_FILEPATH} ${SCANTWOPERMPATH} ${PERMUTATIONS_PER_JOB} $jobs ${RQTLCROSSPATH} ${CROSS}
done

# Combine scantwo permutations
Rscript ${COMBINESCANTWOPERM_R_FILEPATH} ${SCANTWOPERMPATH} ${COMBINESCANTWOPERMPATH}
