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
	usage = "usage: %prog --wrfexp=<wrfEXP> [--debug=<debug_level>] [--io_form_grid=<io_form_grid>] [--output=namelist.wps]"
	parser = OptionParser(usage=usage)

	parser.add_option("-d", "--debug", dest="debug_level",
                  help="An integer value indicating which different types of debug messages to print", metavar="debug_level")

	parser.add_option("-o", "--output", dest="geogrid_namelist",
                  help="namelist.wps file used by WPS (part to run geogrid.exe)", metavar="geogrid_namelist")

	parser.add_option("-w", "--wrfexp", dest="wrfexp",
                  help="WRF experiment setup file", metavar="wrfexp")

	parser.add_option("-i", "--io_form_grid", dest="io_form_grid",
                  help="output format for geogrid.exe - binary (1), netCDF (2), GRIB (3)", metavar="io_form_grid")

	(options, args) = parser.parse_args()

        if not options.wrfexp:
                parser.error("The experiment setup file is missing!")

        if not options.debug_level:
                debug_level=0
        else:
                debug_level=options.debug_level

        if not options.geogrid_namelist:
		geogrid_namelist='namelist.wps'
	else:
		geogrid_namelist=options.geogrid_namelist

        if not options.io_form_grid:
                io_form_grid='2'
        else:
                io_form_grid=options.io_form_grid

        outputdir = os.path.dirname(geogrid_namelist)
        if not os.path.exists(outputdir):
                os.mkdir(outputdir)

        new_file = open(geogrid_namelist,'w+')
        old_file = open(options.wrfexp)
        start=False
        for line in old_file:
                if 'WRF_EXPID' in line:
                    start=True
                elif '&share' in line:
                    new_file.write('&share'+'\n')
                    new_file.write('debug_level='+debug_level.strip()+','+'\n')
                    new_file.write('io_form_geogrid='+io_form_grid+','+'\n')
                elif start:
                    tmp = line.replace('\n','')
                    if tmp.rstrip():
                       new_file.write(tmp.strip()+'\n')

        new_file.close()


if __name__ == "__main__":
    main()
