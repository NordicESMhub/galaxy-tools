#!/usr/bin/env bash

WORKDIR=$1
CASENAME=$2
RESDIR=$3
INFO_FILE=$4

echo "===================================================================="
echo "                Save restarts for CESM run                          " 
echo "===================================================================="

nb_nc=$(find $WORKDIR -type f -name "${CASENAME}.*.r*.*.nc" | wc -l)
nb_bin=$(find $WORKDIR -type f -name "${CASENAME}.*.r*.*.bin" | wc -l)
nb_i=$(find $WORKDIR -type f -name "${CASENAME}.*.i*.*.nc" | wc -l)
nb_rp=$(find $WORKDIR -type f -name "rpointer.*" | wc -l)
    
if [[ $nb_nc -gt 0 ]]; then 
    cp $WORKDIR/${CASENAME}.*.r*.*.nc $RESDIR/ 2>>$INFO_FILE
fi
if [[ $nb_bin -gt 0 ]]; then 
    cp $WORKDIR/${CASENAME}.*.r*.*.bin $RESDIR/ 2>>$INFO_FILE
fi
if [[ $nb_i -gt 0 ]]; then 
    cp $WORKDIR/${CASENAME}.*.i*.*.nc $RESDIR/ 2>>$INFO_FILE
fi
if [[ $nb_rp -gt 0 ]]; then 
    cp $WORKDIR/rpointer.* $RESDIR/ 2>>$INFO_FILE
fi
echo "Restart saved."
