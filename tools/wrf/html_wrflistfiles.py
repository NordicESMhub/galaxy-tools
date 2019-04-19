#!/usr/bin/env python
#
# (C) Copyright 2015 UIO.
#
# Creation: June 2015 - Anne Fouilloux - University of Oslo
#

import os
from optparse import OptionParser


def main():
    usage = "usage: %prog [--inputdir=input_directory]" \
            "[--html=output_filename] [--header=header_file]"

    parser = OptionParser(usage=usage)
    msg = "root directory for listing input files"
    parser.add_option("-i", "--inputdir", dest="inputdir",
                      help=msg,
                      metavar="inputdir")
    msg = "html output filename containing the list of files (recursive)"
    parser.add_option("--html", dest="output_filename", default="listing.html",
                      help=msg,
                      metavar="output_filename")
    msg = "html header filename containing header information"
    parser.add_option("--header", dest="header_file", default="",
                      help=msg,
                      metavar="header_file")
    (options, args) = parser.parse_args()

    if not options.inputdir:
        inputdir = os.getcwd()
        print(inputdir)
    else:
        inputdir = options.inputdir

# Change to workging directory
    os.chdir(inputdir)

    with open(options.output_filename, "w") as theFile:
        theFile.write('<?xml version="1.0" encoding="utf-8" ?>\n')
        msg = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"'
        msg += ' "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n'
        theFile.write(msg)
        msg = '<html xmlns="http://www.w3.org/1999/xhtml"'
        msg += ' xml:lang="en" lang="en">\n'
        theFile.write(msg)
        if len(options.header_file) > 0:
            f = open(options.header_file)
            lines = f.readlines()
            f.close()
            for line in lines:
                theFile.write(line+'\n')

        theFile.write("<body>\n")
        theFile.write("<h2>List of files</h2>\n")
        theFile.write('<div>\n')
        theFile.write('  <ul>\n')

        for dirName, subdirList, fileList in os.walk("./"):
            for fname in fileList:
                fullname = os.path.join(dirName, fname)
                msg = '<li><a href="' + fullname + '">' + fullname
                msg += '</a>  <a href="[download]' + fullname
                msg += '">[download]</a></li>\n'
                theFile.write(msg)
        theFile.write("    </ul>\n")

        theFile.write("</body>\n")
        theFile.write("</html>\n")


if __name__ == "__main__":
    main()
