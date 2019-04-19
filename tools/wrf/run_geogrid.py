#!/usr/bin/python

import os
import shutil
import sys
from tempfile import mkstemp
from optparse import OptionParser


def set_wps_geog(name, subst, wps_home, exp_rundir):
    print(name)
    print(subst)
    # Create temp file
    fh, abs_path = mkstemp()
    new_file = open(abs_path, 'w')
    old_file = open(name)
    is_geog_data_path = False
    for line in old_file:
        if 'geog_data_path' in line or 'GEOG_DATA_PATH' in line:
            newline1 = ' opt_geogrid_tbl_path = ' + "'" + exp_rundir + "/',\n"
            newline2 = ' geog_data_path = ' + "'" + subst + "',\n"
            print(newline1)
            new_file.write(newline1)
            new_file.write(newline2)
            is_geog_data_path = True
        elif 'opt_geogrid_tbl_path' in line:
            print("""Removed user-defined opt_geogrid_tbl_path;
                     file copied in experiment directory""")
        else:
            new_file.write(line)

    # close temp file
    new_file.close()
    old_file.close()
    if not is_geog_data_path:
        # We need to add it as it has never been here
        new_file = open(abs_path, 'w+')
        old_file = open(name)
        for line in old_file:
            if '&geogrid' in line:
                newline1 = ' opt_geogrid_tbl_path = '
                newline1 += "'" + exp_rundir + "/',\n"
                newline2 = ' geog_data_path = ' + "'" + subst + "',\n"
                new_file.write('&geogrid\n')
                new_file.write(newline1)
                new_file.write(newline2)
            elif 'opt_geogrid_tbl_path' in line:
                print("""Removed user-defined opt_geogrid_tbl_path;
                         file copied in experiment directory""")
            else:
                new_file.write(line)

        old_file.close()
        new_file.close()
    os.close(fh)
    # Remove original file
    os.remove(name)
    # Move new file
    shutil.move(abs_path, name)


def set_tbl(exp_rundir, tblname):
    default_path = '/cluster/software/VERSIONS/wrf/3.6.1/WPS'
    wps_home = os.getenv('WPS_HOME', default_path)

    if not tblname:
        tblname = 'GEOGRID.TBL'

    # GEOGRID.TBL is given with full path
    if os.path.isfile(tblname):
        geogrid_tbl = tblname
    elif os.path.isfile(exp_rundir + '/' + tblname):
        # tblname file present in exp_rundir
        geogrid_tbl = exp_rundir + '/' + tblname
    elif os.path.isfile(wps_home + '/geogrid/' + tblname):
        # tblname file present in exp_rundir
        geogrid_tbl = wps_home + '/geogrid/' + tblname
    else:
        geogrid_tbl = wps_home + '/geogrid/GEOGRID.TBL'

    print(geogrid_tbl)
    if not os.path.isfile(geogrid_tbl):
        print("Error geogrid TBL file not found" + geogrid_tbl)
        sys.exit(0)

    check_file = (os.path.basename(geogrid_tbl) == "GEOGRID.TBL")
    check_dir = os.path.dirname(geogrid_tbl) == exp_rundir
    if check_file and check_dir:
        print("File " + geogrid_tbl + " is being used for geogrid.exe...")
    else:
        shutil.copy2(geogrid_tbl, exp_rundir + '/GEOGRID.TBL')


def main():
    usage = "usage: %prog --path namelist.wps_directory " \
            "--expid experiment_identifier [--version=wrf_version] " \
            "[--wps_geog WPS_GEOG] [--tbl GEOGRID.TBL]"
    parser = OptionParser(usage=usage)
    parser.add_option("-p", "--path", dest="path",
                      help="location of namelist.wps",
                      metavar="namelist.wps")
    parser.add_option("-w", "--wps_geog", dest="wps_geog",
                      help="location of terrestrial input data",
                      metavar="WPS_GEOG")
    parser.add_option("-i", "--expid", dest="expid",
                      help="Experiment identifier", metavar="expid")
    parser.add_option("-t", "--tbl", dest="geogrid_tbl",
                      help="GEOGRID.TBL file for running geogrid.exe",
                      metavar="geogrid_tbl")
    parser.add_option("-v", "--version", dest="wrf_version",
                      help="WPS/WRF version", metavar="wrf_version")

    (options, args) = parser.parse_args()

    if not options.path:
        parser.error("the location of namelist.wps needs to be specified")
    if not options.expid:
        parser.error("the experiment identifier is missing!")

    if not options.wps_geog:
        wps_geog = os.getenv('WPS_GEOG_PATH')
    else:
        wps_geog = options.wps_geog

    namelist_wps = options.path + '/namelist.wps'
    if not os.path.isfile(namelist_wps):
        parser.error("the file namelist.wps does not exist in "
                     + namelist_wps)

    if not options.wrf_version:
        # load default WRF version
        module('load', 'wrf')
    else:
        module('load', 'wrf/' + options.wrf_version.strip())

    # set default environment
    default_path = '/cluster/software/VERSIONS/wrf/3.6.1/WPS'
    wps_home = os.getenv('WPS_HOME', default_path)
    username = os.getenv('USER')
    rundir = os.getenv('RUNDIR', '/work/users/'+username)
    exp_rundir = rundir + '/' + options.expid
    # copy namelist.wps in exp_rundir
    if not os.path.exists(exp_rundir):
        os.makedirs(exp_rundir)
    shutil.copy2(namelist_wps, exp_rundir)
    new_namelist_wps = exp_rundir + '/namelist.wps'

    # copy GEOGRID.TBL in exp_rundir
    set_tbl(exp_rundir, options.geogrid_tbl)

    # set geog_data_path in namelist.wps
    set_wps_geog(new_namelist_wps, wps_geog, wps_home, exp_rundir)
    # Run geogrid.exe
    os.chdir(exp_rundir)
    command = 'geogrid.exe '
    os.system(command)


if __name__ == "__main__":
    exec(open("/usr/share/Modules/init/python.py").read())
    main()
