#!/usr/bin/python
#
# Anne Fouilloux
# University of Oslo, Norway
# 2015

import os
import shutil
from optparse import OptionParser


def main():
    usage = "usage: %prog --type=<WRF|WRFCHEM> [--output=GEOGRID.TBL] " \
            "[--version=wrf_version]"
    parser = OptionParser(usage=usage)

    parser.add_option("-t", "--type", dest="wrf_type",
                      help="WRF or WRF CHEM", metavar="debug_level")

    parser.add_option("-o", "--output", dest="geogrid_tbl",
                      help="WPS geogrid table (GEOGRID.TBL) run geogrid.exe",
                      metavar="geogrid_tbl")

    parser.add_option("-v", "--version", dest="wrf_version",
                      help="WPS/WRF version", metavar="wrf_version")

    (options, args) = parser.parse_args()

    if not options.wrf_type:
        parser.error("The experiment type (WRF/WRFCHEM) is missing!")

    if not options.geogrid_tbl:
        geogrid_tbl = 'GEOGRID.TBL'
    else:
        geogrid_tbl = options.geogrid_tbl

    outputdir = os.path.dirname(geogrid_tbl)
    if not os.path.exists(outputdir):
        os.mkdir(outputdir)

    if not options.wrf_version:
        # load default WRF version
        module('load', 'wrf')
    else:
        module('load', 'wrf/' + options.wrf_version.strip())

    default_path_suffix = '/cluster/software/VERSIONS/wrf/'
    default_path = default_path_suffix + str(options.wrf_version)
    wps_home = os.getenv('WPS_HOME', default_path + '/WPS')
    if options.wrf_type == "CHEM":
        old_file = wps_home + '/geogrid/GEOGRID.TBL.ARW_CHEM'
    else:
        old_file = wps_home + '/geogrid/GEOGRID.TBL.ARW'

    print('Default GEOGRID.TBL: ', geogrid_tbl)
    shutil.copy2(old_file, geogrid_tbl)


if __name__ == "__main__":
    exec(open("/usr/share/Modules/init/python.py").read())
    main()
