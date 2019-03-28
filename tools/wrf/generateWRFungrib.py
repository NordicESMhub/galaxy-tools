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
	usage = "usage: %prog --WRFexp=WRFexp [--out_format=WPS|SI|MM5] [--prefix=prefix] [--output=ungrib_namelist]"
	parser = OptionParser(usage=usage)

	parser.add_option("--WRFexp", dest="WRFexp",
                  help="WRF experiment setup file", metavar="WRFexp")

	parser.add_option("--out_format", dest="out_format",
                  help="select the format of the intermediate data to be written by ungrib", metavar="out_format")

	parser.add_option("--prefix", dest="prefix",
                  help="prefix of the intermediate meteorological data files", metavar="prefix")

	parser.add_option("-i", "--interval_seconds", dest="interval_seconds",
                  help="The integer number of seconds between time-varying meteorological input files", metavar="interval_seconds")

	parser.add_option("-o", "--output", dest="ungrib_namelist",
                  help="ungrib_namelist file used by WPS (part of namelist.wps)", metavar="ungrib_namelist")

	(options, args) = parser.parse_args()

        if not options.WRFexp:
		parser.error("the WRFexp file is missing!")

        if not options.out_format:
		out_format='WPS'
	else:
		out_format=options.out_format

        if not options.prefix:
		prefix='FILE'
	else:
		prefix=options.prefix

        if not options.ungrib_namelist:
		ungrib_namelist='ungrib.nml'
	else:
		ungrib_namelist=options.ungrib_namelist

        if not options.interval_seconds:
		interval_seconds='21600'
	else:
		interval_seconds=options.interval_seconds

        new_file = open(ungrib_namelist,'a')
        old_file = open(options.WRFexp)
        start_date_list = []
        end_date_list = []
        for line in old_file:
                if 'max_dom' in line:
                        tmp=line.split('=')
                        print "max_dom= ", tmp[1].replace('\n','')
                        max_dom=tmp[1].replace('\n','')
                elif 'start_date' in line:
                        tmp=line.split('=')
                        start_date_list.append(tmp[1].replace('\n',''))
                elif 'end_date' in line:
                        tmp=line.split('=')
                        end_date_list.append(tmp[1].replace('\n',''))
        old_file.close()
        new_file.write("&share\nmax_dom=" + str(max_dom) + "\n")
        newline='start_date = ' 
        for val in start_date_list:
              newline = newline + ' ' + str(val) 
        print "START DATE: " + newline
        new_file.write(newline + '\n')
        newline='end_date = ' 
        for val in end_date_list:
              newline = newline + ' ' + str(val) 
        print "END DATE: " + newline
        new_file.write(newline + '\n')
        new_file.write("interval_seconds = " + interval_seconds + ",\n")
        new_file.write("/\n\n")

# write ungrib section
        new_file.write("&ungrib\nout_format ='" + str(out_format) + "',\n")
        new_file.write("prefix ='" + str(prefix) + "',\n")
        new_file.write('/\n')
#close temp file
        new_file.close()


if __name__ == "__main__":
    main()
