#!/usr/bin/env bash

if [ -f *.tar.gz ]; then
   tar zxvf  *.tar.gz
   cat *.grib > tmp.grib
   cdo setgridtype,regular tmp.grib tmpg.grib
   cdo -f nc -t ecmwf copy tmpg.grib tmp.nc
elif [ -f *.zip ]; then
   unzip *.zip
   cat *.grib > tmp.grib
   cdo setgridtype,regular tmp.grib tmpg.grib
   cdo -f nc -t ecmwf copy tmpg.grib tmp.nc
elif [ -f *.grib ]; then
   cdo -f nc -t ecmwf copy *.grib tmp.nc
elif [ -f *.nc ]; then
   mv *.nc tmp.nc
else
   echo "No data found! Check your request and/or credentials."
fi
