#!/bin/bash
# Job name:
# get ECMWF data for running WRF
#
#set -x
ulimit -s unlimited

#################################################################################################

echo "Number of parameters: $#"
echo "version: $1"
echo "WRFexp: $2"
echo "datatype: $3"
echo "times: $4"
echo "area: $5"
echo "sfc_params: $6"
echo "3D_params: $7"
echo "outputdir: $8"
echo "outfile: $9"
echo "levtype: ${10}"

version=$1
WRFexp=$2
datatype=$3
times=$4
area=$5
params_sfc=$6
params_3D=$7
outputdir=$8
outfile=$9
levtype=${10}

if [ "$#" -ge 11 ]; then
  pl=${11}
  echo "Levels: ${11}"
else
  pl=""
  echo "Retrieve all available levels"
fi

# copy setup file in working directory
export WRF_EXPID=`grep WRF_EXPID $WRFexp | awk -F= '{print $2}'`
export WRF_START_DATE=`grep start_date $WRFexp | awk -F= '{print $2}' | awk -F_ '{print $1}' | sed "s/'//g" | sed "s/-//g" | sed "s/ //g"`
export WRF_END_DATE=`grep end_date $WRFexp | awk -F= '{print $2}' | awk -F_ '{print $1}' | sed "s/'//g" | sed "s/-//g" | sed "s/ //g"`

# create output directory
mkdir -p $outputdir/$WRF_EXPID

# to be fixed. Each user must have .ecmwfapirc?

cp $WRF_HOME/../bin/.ecmwfapirc $outputdir/$WRF_EXPID/.ecmwfapirc

cat $outputdir/$WRF_EXPID/.ecmwfapirc

date="${WRF_START_DATE}/to/${WRF_END_DATE}"
sfcName="ERA-Int_sfc_${WRF_START_DATE}_to_${WRF_END_DATE}.grib"
plName="ERA-Int_pl_${WRF_START_DATE}_to_${WRF_END_DATE}.grib"
# list all created files
cat  >> header.html  << EOF
<head>
   <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
   <title><h1><b>Collection of GRIB files for running WRF model</b></h1></title>

   <p><font size="4" style="font-size: 14pt"><i>expid: $WRF_EXPID</i></font></p>
   <p><font size="4" style="font-size: 14pt"><i>version: $WRFversion</i></font></p>
   <p><font size="4" style="font-size: 14pt"><i>WRF_KPP: $WRF_KPP</i></font></p>
   <p><br></br></p>
   <h2>Logs</h2>
   <ul>
   <li><a href="${WRF_EXPID}.wrfexp">${WRF_EXPID}.wrfexp</a>  <a href="[download]${WRF_EXPID}.wrfexp">[download]</a></li>
   </ul>
   <p><br></br></p>
</head>
EOF

if [ "$datatype" == "ERA-40" ] ; then
   dataset="era40"
   class="e4"
   stream="oper"
   grid="128"
elif [ "$datatype" == "ERA-15" ] ; then
   dataset="era15"
   class="er"
   stream="oper"
   grid="128"
elif [ "$datatype" == "ERA-20c" ] ; then
   dataset="era20c"
   class=""
   stream="oper"
   grid="128"
elif [ "$datatype" == "ERA-interim" ] ; then
   dataset="interim"
   class="ei"
   stream="oper"
   grid="128"
elif [ "$datatype" == "MACC-reanalysis" ] ; then
   dataset="macc"
   class="mc"
   stream="oper"
   grid="128"
else
   echo "Error: datatype $datatype is unknown..."
fi
current_pwd=`pwd`
cd $outputdir/$WRF_EXPID
TFILE="$(basename $0).$$.tmp"

cat  > $TFILE  << EOF
#!/usr/bin/env python
#
# (C) Copyright 2012-2013 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.
#

from ecmwfapi import ECMWFDataServer

# To run this example, you need an API key
# available from https://api.ecmwf.int/v1/key/

server = ECMWFDataServer()

server.retrieve({
          'dataset' : "$dataset",
          'date'    : "$date",
          'time'     : "$times",
          'step'     : "0",
          'stream'   : "$stream",
          'levtype'  : "sfc",
          'levelist' : "all",
          'type'     : "an",
          'grid'     : "$grid",
          'param'    : "$params_sfc",
          'target'   : "${sfcName}",
EOF
if [[ "$class" = "" ]] ; then
cat  >> $TFILE  << EOF
          })
EOF
else
cat  >> $TFILE  << EOF
          'class'    : "$class",
          })
EOF
fi

if [[ "$params_sfc" == "None" ]]; then
  echo "No surface parameters to retrieve..."
else
#AF  python $TFILE
  chmod u+x $TFILE
  ./$TFILE
fi

cat $TFILE

rm -rf $TFILE

cat  > $TFILE  << EOF
#!/usr/bin/env python
#
# (C) Copyright 2012-2013 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.
#

from ecmwfapi import ECMWFDataServer

# To run this example, you need an API key
# available from https://api.ecmwf.int/v1/key/

server = ECMWFDataServer()

server.retrieve({
          'dataset' : "$dataset",
          'date'    : "$date",
          'time'     : "$times",
          'step'     : "0",
          'stream'   : "$stream",
          'levtype'  : "$levtype",
          'levelist' : "$levelist",
          'type'     : "an",
          'grid'     : "$grid",
          'param'    : "$params_3D",
          'target'   : "${plName}",
EOF
if [[ "$class" = "" ]] ; then
cat  >> $TFILE  << EOF
          })
EOF
else
cat  >> $TFILE  << EOF
          'class'    : "$class",
          })
EOF
fi

if [[ "$params_3D" == "None" ]]; then
  echo "No 3D parameters to retrieve..."
else
#AF  python $TFILE
  chmod u+x $TFILE
  ./$TFILE
fi

cat $TFILE
rm -rf $TFILE

html_wrflistfiles.py --inputdir=../ --html=$outfile --header=$current_pwd/header.html

rm -rf $current_pwd/header.html
cp $WRFexp $outputdir/${WRF_EXPID}.wrfexp

