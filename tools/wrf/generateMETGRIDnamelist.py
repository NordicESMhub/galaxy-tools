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
	usage = "usage: %prog --expid=<WRFexpid> --metgrid=<metgrid_script> [--output=namelist.wps]"
	parser = OptionParser(usage=usage)

	parser.add_option("-o", "--output", dest="metgrid_namelist",
                  help="namelist.wps file used by WPS (part to run metgrid.exe)", metavar="metgrid_namelist")

	parser.add_option("-w", "--expid", dest="expid",
                  help="WRF experiment setup file", metavar="expid")

	parser.add_option("-m", "--metgrid", dest="metgrid",
                  help="metgrid script containing information for creating metgrid namelist", metavar="metgrid")

	(options, args) = parser.parse_args()

        if not options.expid:
                parser.error("The experiment identifier is missing!")
        print "generateMETGRIDnamelist.py WRF_EXPID = ", options.expid

        if not options.metgrid:
                parser.error("The metgrid script file is missing!")

        if not options.metgrid_namelist:
		metgrid_namelist='namelist.wps'
	else:
		metgrid_namelist=options.metgrid_namelist

        outputdir = os.path.dirname(metgrid_namelist)
        if not os.path.exists(outputdir):
                os.mkdir(outputdir)

        script_file = open(options.metgrid)
        datapath = []
        fg_name = []
        constants_name = []
        process_only_bdy = ""
        io_form_metgrid = ""
        wrfgeo_path = ""
        for line in script_file:
                if 'fg_name' in line:
                        tmp=line.split('=')
                        fg_name=tmp[1].replace('\n','').split(',')
                elif 'constants_name' in line:
                        tmp=line.split('=')
                        constants_name=tmp[1].replace('\n','').split(',')
                elif 'process_only_bdy' in line:
                        tmp=line.split('=')
                        process_only_bdy=tmp[1].replace('\n','')
                elif 'io_form_metgrid' in line:
                        tmp=line.split('=')
                        io_form_metgrid=tmp[1].replace('\n','')
                elif 'wrfgeo_path' in line:
                        tmp=line.split('=')
                        wrfgeo_path=tmp[1].replace('\n','')
                elif 'WPS_' in line:
                        tmp=line.split('=')
                        datapath.append(tmp[1].replace('\n',''))

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
        script_file.close()
        interval_seconds=-1
        for path in  datapath:
           datanml = path.strip() + '/ungrib.nml'
           nmlfile = open(datanml)
           for line in nmlfile:
               if 'interval_seconds' in line:
                     tmp=line.split('=')
                     newinterval_seconds=int(tmp[1].replace('\n','').replace(',','').strip())
                     if interval_seconds == -1: 
                         interval_seconds = newinterval_seconds
                     if (interval_seconds != newinterval_seconds):
                        print "Error: interval_seconds should be identical among the datasets!", interval_seconds, newinterval_seconds
           nmlfile.close()

        geogrid_filename = wrfgeo_path.strip() + '/namelist.wps'
        print 'geogrid_filename = ', geogrid_filename
        geogrid_namelist = open(geogrid_filename)
        new_file = open(metgrid_namelist,'w')
        start_share=False
        for line in geogrid_namelist:
           if '&share' in line:
                 start_share=True
                 new_file.write('&share'+'\n')
                 new_file.write('interval_seconds = '+ str(interval_seconds) + ',\n')
#AF           elif '&geogrid' in line:
#AF                 start_share = False
#AF           elif start_share and '&geogrid' not in line:
           elif start_share and 'opt_geogrid_tbl_path' not in line:
                 new_file.write(line)
# write metgrid section in new namelist.wps
        geogrid_namelist.close()
        new_file.write("\n &metgrid\n")                
        new_file.write("io_form_metgrid = " + io_form_metgrid + ",\n")                
        new_file.write("process_only_bdy = " + process_only_bdy + ",\n")                
        new_file.write("fg_name = ")                
        for name in fg_name:
           new_file.write("'"+name.strip()+"',")
        new_file.write("\n constants_name = ")                
        for name in constants_name:
           new_file.write("'"+name.strip()+"',")
        new_file.write('\n/\n')
        new_file.close()

# Create symbolic link for all the available datasets
        outputdir = os.path.dirname(metgrid_namelist)
# geogrid file geo_em*
        for dirName, subdirList, fileList in os.walk(wrfgeo_path.strip()+'/'):
          for fname in fileList:
              if len(fname) > 6 and fname[:6] == 'geo_em':
                fullname=os.path.join(dirName, fname)
                print "symbolic link... " + fullname
                os.symlink(fullname, outputdir + '/'+ fname) 
        for path in  datapath:
          for dirName, subdirList, fileList in os.walk(path.strip()+'/' + options.expid.strip() +'/'):
              for fname in fileList:
                if fname != "Vtable":
                  ext = os.path.splitext(fname)[1] 
                  if ext != '.log' and ext != '.nml' and ext != '.wps':
                    fullname=os.path.join(dirName, fname)
                    print "symbolic link... " + fullname
                    os.symlink(fullname, outputdir + '/'+ fname) 

if __name__ == "__main__":
    main()
