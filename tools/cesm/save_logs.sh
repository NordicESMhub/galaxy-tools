#!/usr/bin/env bash

WORKDIR=$1
LOGDIR=$2
INFO_FILE=$3

echo "===================================================================="
echo "               Save logfiles from CESM run                          " 
echo "===================================================================="

for log_type in atm cesm cpl lnd rof; do
    nb=$(find $WORKDIR -type f -name "$log_type.log.*" | wc -l)
    nbz=$(find $WORKDIR -type f -name "$log_type.log.*.gz" | wc -l)
    
    if [[ $nb -gt 0 ]]; then 
        if [[ $nb -gt 0 ]]; then 
            gunzip $1/${log_type}.log.*.gz
        fi
        cat $1/${log_type}.* > $2/${log_type}.txt 2>>$INFO_FILE
    fi
done

echo "Logfiles saved."
