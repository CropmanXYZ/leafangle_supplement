SCANTWOPERM_R_FILEPATH=$1
SCANTWOPERMPATH=$2
PERMUTATIONS_PER_JOB=$3
JOBNUMBER=$4
RQTLCROSSPATH=$5
CROSS=$6

Rscript ${SCANTWOPERM_R_FILEPATH} ${SCANTWOPERMPATH} ${PERMUTATIONS_PER_JOB} ${JOBNUMBER} ${RQTLCROSSPATH} ${CROSS}
