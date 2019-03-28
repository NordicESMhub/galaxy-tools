#!/usr/bin/python

import os
from optparse import OptionParser

def main():
	usage = "usage: %prog --path namelist_wps_dir  [--version=wrf_version]"
	parser = OptionParser(usage=usage)
	parser.add_option("-p", "--path", dest="path",
                  help="location of namelist.wps", metavar="FILE")
	parser.add_option("-v", "--version", dest="wrf_version",
                  help="WPS/WRF version", metavar="wrf_version")

	(options, args) = parser.parse_args()

        if not options.wrf_version:
# load default WRF version
                module('load','wrf')
        else:
                module('load','wrf/'+options.wrf_version.strip())

	wps_home=os.getenv('WPS_HOME', '/cluster/software/VERSIONS/wrf/3.6.1/WPS')

        print options.path
        os.chdir(options.path)
	command = 'module load ncl/6.2.0; ncl ' + wps_home + '/util/plotgrids_new.ncl'


	os.system(command)

if __name__ == "__main__":
    execfile('/usr/share/Modules/init/python.py')
    main()
