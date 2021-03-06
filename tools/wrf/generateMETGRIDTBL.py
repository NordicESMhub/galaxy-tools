#!/usr/bin/python
# Anne Fouilloux
# University of Oslo, Norway
# 2015

import os
import shutil
from optparse import OptionParser


def main():
    usage = "usage: %prog --type=<WRF|WRFCHEM> [--output=METGRID.TBL] " \
            "[--version=wrf_version]"
    parser = OptionParser(usage=usage)

    parser.add_option("-t", "--type", dest="wrf_type",
                      help="WRF or WRF CHEM", metavar="debug_level")

    parser.add_option("-o", "--output", dest="metgrid_tbl",
                      help="WPS metgrid table (METGRID.TBL) (run metgrid.exe)",
                      metavar="metgrid_tbl")

    parser.add_option("-v", "--version", dest="wrf_version",
                      help="WPS/WRF version", metavar="wrf_version")

    (options, args) = parser.parse_args()

    if not options.wrf_type:
        parser.error("The experiment type (WRF/WRFCHEM) is missing!")

    if not options.metgrid_tbl:
        metgrid_tbl = 'METGRID.TBL'
    else:
        metgrid_tbl = options.metgrid_tbl

    outputdir = os.path.dirname(metgrid_tbl)
    if not os.path.exists(outputdir):
        os.mkdir(outputdir)

    if not options.wrf_version:
        # load default WRF version
        module('load', 'wrf')
    else:
        module('load', 'wrf/' + options.wrf_version.strip())

    default_path_prefix = '/cluster/software/VERSIONS/wrf/'
    default_path = default_path_prefix + str(options.wrf_version)
    wps_home = os.getenv('WPS_HOME', default_path + '/WPS')
    old_file = wps_home + '/metgrid/METGRID.TBL.ARW'

    print('Default METGRID.TBL: ', metgrid_tbl)
    shutil.copy2(old_file, metgrid_tbl)


if __name__ == "__main__":
    exec(open("/usr/share/Modules/init/python.py").read())
    main()
