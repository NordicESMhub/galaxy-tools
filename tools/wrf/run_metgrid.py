#!/usr/bin/python

import os
import sys
import shutil
from tempfile import mkstemp
from optparse import OptionParser


def main():
	usage = "usage: %prog --expid expid --tbl METGRID.TBL [--version=wrf_version]"
	parser = OptionParser(usage=usage)

	parser.add_option("-i", "--expid", dest="expid",
                  help="Experiment identifier", metavar="expid")

	parser.add_option("-t", "--tbl", dest="metgrid",
                  help="METGRIB.TBL file", metavar="metgrid")

	parser.add_option("-v", "--version", dest="wrf_version",
                  help="WPS/WRF version", metavar="wrf_version")

	(options, args) = parser.parse_args()

        if not options.expid:
		parser.error("the experiment identifier is missing!")

        if not options.metgrid:
		wps_home=os.getenv('WPS_HOME','/cluster/software/VERSIONS/wrf/3.6.1/WPS')
		metgrid=wps_home + '/metgrid/METGRID.TBL'
	else:
		metgrid=options.metgrid
	
	if not os.path.isfile(metgrid):
                print "Error METGRID.TBL file not found"
                sys.exit(0)

        if not options.wrf_version:
# load default WRF version
                module('load','wrf')
        else:
                module('load','wrf/'+options.wrf_version.strip())

        username=os.getenv('USER')
        rundir=os.getenv('RUNDIR','/work/users/'+username)
        exp_rundir=rundir+'/'+options.expid

	print metgrid
        if os.path.basename(metgrid) == "METGRID.TBL" and os.path.dirname(metgrid) == exp_rundir + '/metgrid':
                print "File " + metgrid + " is being used for metgrid.exe..."
        else:
		if not os.path.exists(exp_rundir + '/metgrid'):
			os.mkdir(exp_rundir + '/metgrid')
                shutil.copy2(metgrid,exp_rundir + '/metgrid/METGRID.TBL')

        os.chdir(exp_rundir)

# Execute ungrib.exe
        command ='metgrid.exe'

        os.system(command)
if __name__ == "__main__":
    execfile('/usr/share/Modules/init/python.py')
    main()
