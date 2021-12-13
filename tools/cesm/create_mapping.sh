#!/usr/bin/env bash

echo "=========================================="
echo "     Create symbolic link for input data  "
echo "=========================================="

echo "Search for $2..."

create_link=$(grep $2 $3)
dir=$(dirname $create_link)

echo "mkdir -p inputdata/$dir"
mkdir -p inputdata/$dir

echo "ln -s $1 inputdata/$create_link"
ln -s $1 inputdata/$create_link
