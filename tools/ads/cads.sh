#!/usr/bin/env bash

if [ -f download.tar.gz ]; then
   tar zxvf  download.tar.gz
   cat *.grib > tmp.grib
   cdo setgridtype,regular tmp.grib tmpg.grib
   cdo -f nc -t ecmwf copy tmpg.grib tmp.nc
elif [ -f download.zip ]; then
   unzip download.zip
   cat *.grib > tmp.grib
   cdo setgridtype,regular tmp.grib tmpg.grib
   cdo -f nc -t ecmwf copy tmpg.grib tmp.nc
elif [ -f download.grib ]; then
   cdo -f nc -t ecmwf copy download.grib tmp.nc
elif [ -f download.nc ]; then
   mv download.nc tmp.nc
else
   echo "No data found! Check your request and/or credentials."
fi
