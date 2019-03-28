#!/bin/bash
# Job name:
# run ungrib.exe
#
#set -x
ulimit -s unlimited

#################################################################################################

echo "Number of parameters: $#"
echo "version: $1"
echo "WRF: $2"
echo "WRFexp: $3"
echo "out_format: $4"
echo "Vtable: $5"
echo "inputdir: $6"
echo "interval_seconds: $7"
echo "prefix: $8"
echo "outputdir: $9"
echo "outfile: ${10}"
echo "Vtable type: |${11}|"

WRFversion=$1
WRFtype=$2
WRFexp=$3
out_format=$4
Vtable=$5
inputdir=$6
interval_seconds=$7
prefix=$8
outputdir=$9
outfile=${10}
vtable_type=${11}


# copy setup file in working directory
export WRF_EXPID=`grep WRF_EXPID $WRFexp | awk -F= '{print $2}'`
export WRF_START_DATES=`grep start_date $WRFexp | awk -F= '{print $2}'  | sed "s/'//g" | sed "s/ //g" |  sed "s/,$//g"`
export WRF_END_DATES=`grep end_date $WRFexp | awk -F= '{print $2}'  | sed "s/'//g" | sed "s/ //g" |  sed "s/,$//g"`

module load wrf/$WRFversion

# create output directory
mkdir -p $outputdir/$WRF_EXPID

# Generate WPS namelist for running ungrib
generateWRFungrib.py --WRFexp=$WRFexp --out_format=$out_format --prefix=$prefix --interval_seconds=$interval_seconds -o $outputdir/ungrib.nml

echo "===================================="
cat $outputdir/ungrib.nml
echo "===================================="

# Vtable
if [[ "$Vtable_type" == "default" ]] ; then
# add path to filename
  vtable_file=$WPS_HOME/ungrib/Variable_Tables/$Vtable
else
  vtable_file=$Vtable
fi 

echo "WRF_EXPID: $WRF_EXPID"
echo "WRF_START_DATES: $WRF_START_DATES"
echo "WRF_END_DATES: $WRF_END_DATES"
echo "Vtable file: $vtable_file"

# copy ungrib.nml to namelist.wps (used by ungrib.exe)
cp $outputdir/ungrib.nml $outputdir/$WRF_EXPID/namelist.wps

export RUNDIR=$outputdir
# run ungrib.exe
UNGRIB_EXE=`which ungrib.exe`
echo "ungrib.exe is $UNGRIB_EXE"

run_ungrib.py --expid  $WRF_EXPID                     \
              --start_date $WRF_START_DATES           \
              --end_date $WRF_END_DATES               \
              --interval_seconds $interval_seconds    \
              --prefix $prefix                        \
              --vtable $vtable_file                   \
              --datadir $inputdir/$WRF_EXPID

# Do not keep namelist.wps (we keep ungrib.nml)
mv $outputdir/$WRF_EXPID/namelist.wps $outputdir/ungrib.nml
mv $outputdir/$WRF_EXPID/*.log $outputdir/.
mv $outputdir/$WRF_EXPID/Vtable $outputdir/.

# Remove intermediate files
rm $outputdir/$WRF_EXPID/GRIBFILE.*

# list all created files
cat  >> header.html  << EOF
<head>
   <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
   <title><h1><b>WPS file obtained after running ungrib.exe</b></h1></title>

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

current_pwd=`pwd`
cd $outputdir/$WRF_EXPID

html_wrflistfiles.py --inputdir=../ --html=$outfile --header=$current_pwd/header.html

rm -rf $current_pwd/header.html
cp $WRFexp $outputdir/${WRF_EXPID}.wrfexp

