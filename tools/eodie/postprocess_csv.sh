#!/usr/bin/env bash

WORKDIR=$1
RESDIR=$2

echo "===================================================================="
echo "               Convert EODIE csv to tabular                         " 
echo "===================================================================="

nb_csv=$(find $WORKDIR -type f -name "*.csv" | wc -l)
echo "Number of csv file to convert: $nb_csv"
if [[ $nb_csv -gt 0 ]]; then
    echo "Start"
    for infile in $WORKDIR/*.csv; do
        echo "processing $infile"
        sed -i.bak -e "s/,/\t/g" $infile
        mv $infile $RESDIR/.
    done
fi

echo "EODIE Tabular saved."
