#!/usr/bin/python
# Anne Fouilloux
# University of Oslo, Norway
# 2015

import os
import shutil
import glob
from tempfile import mkstemp
from optparse import OptionParser

def main():
	usage = "usage: %prog --type=<WRF|WRFCHEM> [--output=GEOGRID.TBL] [--version=wrf_version]"
	parser = OptionParser(usage=usage)

	parser.add_option("-t", "--type", dest="wrf_type",
                  help="WRF or WRF CHEM", metavar="debug_level")

	parser.add_option("-o", "--output", dest="geogrid_tbl",
                  help="geogrid table (GEOGRID.TBL) used by WPS (part to run geogrid.exe)", metavar="geogrid_tbl")

	parser.add_option("-v", "--version", dest="wrf_version",
                  help="WPS/WRF version", metavar="wrf_version")

	(options, args) = parser.parse_args()

        if not options.wrf_type:
                parser.error("The experiment type (WRF/WRFCHEM) is missing!")

        if not options.geogrid_tbl:
		geogrid_tbl='GEOGRID.TBL'
	else:
		geogrid_tbl=options.geogrid_tbl

        outputdir = os.path.dirname(geogrid_tbl)
        if not os.path.exists(outputdir):
                os.mkdir(outputdir)

        if not options.wrf_version:
# load default WRF version
                module('load','wrf')
        else:
                module('load','wrf/'+options.wrf_version.strip())

        wps_home=os.getenv('WPS_HOME', '/cluster/software/VERSIONS/wrf/'+str(options.wrf_version)+'/WPS')
        if options.wrf_type=="CHEM" :
          old_file=wps_home+'/geogrid/GEOGRID.TBL.ARW_CHEM'
        else:
          old_file=wps_home+'/geogrid/GEOGRID.TBL.ARW'

        print 'Default GEOGRID.TBL: ', geogrid_tbl
        shutil.copy2(old_file,geogrid_tbl)


if __name__ == "__main__":
    execfile('/usr/share/Modules/init/python.py')
    main()
