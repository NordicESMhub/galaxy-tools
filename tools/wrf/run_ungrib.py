#!/usr/bin/python

import os
import sys
import shutil
from tempfile import mkstemp
from optparse import OptionParser


def set_vtable(exp_rundir, vname):
    # vtable is given with full path
    if os.path.isfile(vname):
        vtable = vname
    elif os.path.isfile(exp_rundir + '/' + vname):
        # vtable file present in exp_rundir
        vtable = exp_rundir + '/' + vname
    else:
        default_path = '/cluster/software/VERSIONS/wrf/3.6.1/WPS'
        wps_home = os.getenv('WPS_HOME', default_path)
        vtable = wps_home + '/ungrib/Variable_Tables/' + vname

    print(vtable)
    if not os.path.isfile(vtable):
        print("Error vtable file not found")
        sys.exit(0)

    check_vtable = (os.path.basename(vtable) == "Vtable")
    check_vtable_dir = (os.path.dirname(vtable) == exp_rundir)
    if check_vtable and check_vtable_dir:
        print("File " + vtable + " is being used for ungrib.exe...")
    else:
        shutil.copy2(vtable, exp_rundir + '/Vtable')


def set_wps_parameters(name, start_date, end_date, interval_seconds, prefix):
    # Create temp file
    fh, abs_path = mkstemp()
    new_file = open(abs_path, 'w')
    old_file = open(name)
    for line in old_file:
        if 'start_date' in line and start_date:
            list_start_date = start_date.split(',')
            newline = " start_date = "
            for sdate in list_start_date:
                newline = newline + "'" + sdate.strip() + "',"
            new_file.write(newline + '\n')
        elif 'end_date' in line and end_date:
            list_end_date = end_date.split(',')
            newline = " end_date = "
            for edate in list_end_date:
                newline = newline + "'" + edate.strip() + "',"
            new_file.write(newline + '\n')
        elif 'interval_seconds' in line and interval_seconds:
            newline = " interval_seconds = " + interval_seconds + ",\n"
            new_file.write(newline)
        elif 'prefix' in line and prefix:
            newline = " prefix = '" + prefix + "',\n"
            new_file.write(newline)
        else:
            new_file.write(line)

    # close temp file
    new_file.close()
    os.close(fh)
    old_file.close()
    # Remove original file
    os.remove(name)
    # Move new file
    shutil.move(abs_path, name)


def main():
    usage = "usage: %prog --expid expid --vtable vtable " \
            "--datadir datadir [--version wrf_version] " \
            "[--start_date startdate] [--end_date enddate] " \
            "[--interval_seconds val] [--prefix FILE]"
    parser = OptionParser(usage=usage)
    parser.add_option("-s", "--start_date", dest="start_date",
                      help=" A list of MAX_DOM character strings " +
                           "of the form 'YYYY-MM-DD_HH:mm:ss' " +
                           "specifying the starting UTC " +
                           "date of the simulation for each domain. ",
                      metavar="startdate")
    parser.add_option("-e", "--end_date", dest="end_date",
                      help="A list of MAX_DOM character strings of " +
                           "the form 'YYYY-MM-DD_HH:mm:ss' specifying " +
                           "the ending UTC date of the simulation for " +
                           " each domain", metavar="enddate")
    parser.add_option("-t", "--interval_seconds", dest="interval_seconds",
                      help="The integer number of seconds between " +
                           "time-varying meteorological input files. " +
                           " No default value.", metavar="interval_seconds")

    parser.add_option("-p", "--prefix", dest="prefix",
                      help="prefix of the intermediate meteorological " +
                           "data files", metavar="FILE")

    parser.add_option("-v", "--vtable", dest="vtable",
                      help="vtable filename", metavar="Vtable")

    parser.add_option("--version", dest="wrf_version",
                      help="WPS/WRF version", metavar="wrf_version")

    parser.add_option("-i", "--expid", dest="expid",
                      help="Experiment identifier", metavar="expid")

    parser.add_option("-d", "--datadir", dest="datadir",
                      help="Directory where input fields can be found",
                      metavar="datadir")

    (options, args) = parser.parse_args()

    if not options.expid:
        parser.error("the experiment identifier is missing!")

    if not options.vtable:
        parser.error("vtable file is missing!")

    if not options.wrf_version:
        # load default WRF version
        module('load', 'wrf')
    else:
        module('load', 'wrf/' + options.wrf_version.strip())

    dirroot = os.path.dirname(options.datadir)
    print(dirroot)
    check_dir = (not os.path.exists(options.datadir))
    checkdir = (check_dir and not os.path.exists(dirroot))
    if not options.datadir or check_dir :
        parser.error("the directory containing input fields is missing!")

    check_start_date = (options.start_date and not options.end_date)
	check_end_date = (options.end_date and not options.start_date)
    if  check_start_date or check_end_date:
        parser.error("both start_date and end_date must be specified!")

    username = os.getenv('USER')
    rundir = os.getenv('RUNDIR', '/work/users/' + username)
    exp_rundir = rundir + '/' + options.expid
    namelist_wps =  exp_rundir + '/namelist.wps'
    # set parameters in namelist.wps if required
    set_wps_parameters(namelist_wps,options.start_date, options.end_date, 
                       options.interval_seconds, options.prefix)

    # copy Vtable in running directory
    set_vtable(exp_rundir, options.vtable)

    # create symbolic links with link_grib.csh
    os.chdir(exp_rundir)
    if not os.path.exists(options.datadir):
        command = 'link_grib.csh ' + options.datadir 
    else:
        command = 'link_grib.csh ' + options.datadir + '/'
    os.system(command)

    # Execute ungrib.exe
    command ='ungrib.exe >& ungrib_data.log'
    os.system(command)


if __name__ == "__main__":
    exec(open("/usr/share/Modules/init/python.py").read())
    main()
