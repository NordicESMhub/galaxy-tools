#!/usr/bin/python

import os
import shutil
import glob
from tempfile import mkstemp
from optparse import OptionParser


def set_inputs(exp_rundir, wrf_path, name, ext):

	if not name:
		dirname=wrf_path
	else:
		dirname=name

        if not os.path.exists(dirname):
		print "Error "+ ext + " files not found in " + dirname
                sys.exit(1)

        if dirname == exp_rundir:
                print ext + " files already in " + exp_rundir +  " ..."
        else:
		print "dirname = " + dirname
		for file in  glob.glob(dirname+'/'+ext): 
			print "file = " + file
			shutil.copy2(file,exp_rundir)


def get_wrf_path(type):
        wrf_home=os.getenv('WRF_HOME')
	if type == 'em_real':
                if not os.path.exists(wrf_home + '/dmpar/WRFV3/test/em_real'):
			return wrf_home + '/test/em_real'
		else:
			return wrf_home + '/dmpar/WRFV3/test/em_real'
	else:
                if not os.path.exists(wrf_home + '/serial/WRFV3/test/' + type):
			return wrf_home + '/test/' + type
		else:
			return wrf_home + '/serial/WRFV3/test/' + type
		

def main():
	usage = "usage: %prog --expid expid [--namelist namelist_input] [--case wrf_case] [--d physics_data_dir] [--npes nprocs]"
	parser = OptionParser(usage=usage)

	parser.add_option("-i", "--expid", dest="expid",
                  help="Experiment identifier", metavar="expid")

	parser.add_option("-n", "--namelist", dest="namelist_input",
                  help="namelist.input file for running WRF", metavar="namelist.input")

	parser.add_option("-c", "--case", dest="wrf_case",
                  help="type of experiment i.e. em_real for data real cases", metavar="wrf_case")

	parser.add_option("-d", "--data_dir", dest="physics_data_dir",
                  help="directory where all model physics data files (*.TBL, *_DATA, *.formatted, tr*t*) can be found for running erf.exe", metavar="physics_data_dir")

	parser.add_option("-p", "--npes", dest="npes",
                  help="number of MPI tasks for running WRF", metavar="npes")

	(options, args) = parser.parse_args()

        username=os.getenv('USER')
        rundir=os.getenv('RUNDIR','/work/users/'+username)
        exp_rundir=rundir+'/'+options.expid
        wrf_home=os.getenv('WRF_HOME')

        if not options.expid:
		parser.error("the experiment identifier is missing!")

        if not options.wrf_case:
		wrf_case='em_real'
	else:
		wrf_case=options.wrf_case

        if not options.npes:
		npes='1'
	else:
		npes=options.npes

	namelist_input=exp_rundir + '/namelist.input'

        if options.namelist_input and (not os.path.isfile(namelist_input) or options.namelist_input != namelist_input):
		shutil.copy2(options.namelist_input,exp_rundir + '/namelist.input')

	if not os.path.isfile(namelist_input):
		parser.error("the file namelist.input does not exist in "+ namelist_input)
        os.chdir(exp_rundir)

# get the right executables
	wrf_path=get_wrf_path(wrf_case)
	print wrf_path

# set-up *.TBL files (GENPARM, LANDUSE, SOILPARM, URBPARM, VEGPARM, MPTABLE) in exp_rundir
	set_inputs(exp_rundir, wrf_path, options.physics_data_dir, '*.TBL')
	set_inputs(exp_rundir, wrf_path, options.physics_data_dir, '*.BIN')

	set_inputs(exp_rundir, wrf_path, options.physics_data_dir, '*_DATA')
	set_inputs(exp_rundir, wrf_path, options.physics_data_dir, '*.formatted')
	set_inputs(exp_rundir, wrf_path, options.physics_data_dir, 'tr*t*')
# Execute wrf.exe

	if os.path.isfile(wrf_path + '/wrf.exe'):
                if int(npes) > 1:
		    command ='module load wrf; ulimit -s unlimited; mpirun ' + wrf_path + '/wrf.exe'
                else:
		    command ='module load wrf; ulimit -s unlimited; ' + wrf_path + '/wrf.exe'

		err=os.system(command)
		if err==0:
			print "wrf.exe done..."
		else:
			print "Error while running wrf.exe. Check logfiles...\n"
			exit(1)

if __name__ == "__main__":
    execfile('/usr/share/Modules/init/python.py')
    module('load','wrf')
    main()
