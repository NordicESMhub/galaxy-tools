#!/usr/bin/python

import os
import shutil
import glob
from tempfile import mkstemp
from optparse import OptionParser


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
                  help="directory where model physics data files (*.TBL, *_DATA, *.formatted, tr*t*) can be found for running erf.exe", metavar="physics_data_dir")
	parser.add_option("-p", "--npes", dest="npes",
                  help="number of MPI tasks for running WRF", metavar="npes")

	(options, args) = parser.parse_args()

        username=os.getenv('USER')
        rundir=os.getenv('RUNDIR','/work/users/'+username)
        exp_rundir=rundir+'/'+options.expid
        wrf_home=os.getenv('WRF_HOME')

        if not options.expid:
		parser.error("the experiment identifier is missing!")

        if not options.npes:
		npes='1'
	else:
		npes=options.npes

        if not options.wrf_case:
		wrf_case='em_real'
	else:
		wrf_case=options.wrf_case

	namelist_input=exp_rundir + '/namelist.input'

        if options.namelist_input and (not os.path.isfile(namelist_input) or options.namelist_input != namelist_input):
		shutil.copy2(options.namelist_input,exp_rundir + '/namelist.input')

	if not os.path.isfile(namelist_input):
		parser.error("the file namelist.input does not exist in "+ namelist_input)
        os.chdir(exp_rundir)

# get the right executables
	wrf_path=get_wrf_path(wrf_case)
	print wrf_path

	if os.path.isfile(wrf_path + '/real.exe'):
                if int(npes) > 1:
		    command ='module load wrf; ulimit -s unlimited; mpirun ' + wrf_path + '/real.exe'
                else:
		    command ='module load wrf; ulimit -s unlimited; ' + wrf_path + '/real.exe'
		err=os.system(command)
		if err==0:
			print "real.exe done...\n"
		else:
			print "Error while running real.exe. Check logfiles...\n"
			exit(1)

	if os.path.isfile(wrf_path + '/ideal.exe'):
		command ='module load wrf; ' + wrf_path + '/ideal.exe'
		err=os.system(command)
		if err==0:
			print "ideal.exe done..."
		else:
			print "Error while running ideal.exe. Check logfiles...\n"
			exit(1)

if __name__ == "__main__":
    execfile('/usr/share/Modules/init/python.py')
    module('load','wrf')
    main()
