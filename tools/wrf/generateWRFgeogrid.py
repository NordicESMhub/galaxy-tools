#!/usr/bin/python
# Anne Fouilloux
# University of Oslo, Norway
# 2015

from optparse import OptionParser


def main():
    usage = "usage: %prog --geogrid=geogrid_info [--output=geogrid_namelist]"
    parser = OptionParser(usage=usage)

    parser.add_option("-g", "--geogrid", dest="geogrid_info",
                      help="Geogrid file containing geogrid information",
                      metavar="geogrid_info")

    parser.add_option("-o", "--output", dest="geogrid_namelist",
                      help="geogrid_namelist file used by WPS (namelist.wps)",
                      metavar="geogrid_namelist")

    (options, args) = parser.parse_args()

    if not options.geogrid_info:
        parser.error("the geogrid file is missing!")

    if not options.geogrid_namelist:
        geogrid_namelist = 'geogrid.nml'
    else:
        geogrid_namelist = options.geogrid_namelist

    new_file = open(geogrid_namelist, 'a')
    old_file = open(options.geogrid_info)
    parent_id_list = []
    parent_grid_ratio_list = []
    i_parent_start_list = []
    j_parent_start_list = []
    e_we_list = []
    e_sn_list = []
    start_date_list = []
    end_date_list = []
    geog_data_res_list = []
    max_dom = 0
    for line in old_file:
        if 'parent_id_' in line:
            max_dom = max_dom+1
        elif 'start_date_' in line:
            tmp = line.split('=')
            start_date_list.append(tmp[1].replace('\n', ''))
        elif 'end_date_' in line:
            tmp = line.split('=')
            end_date_list.append(tmp[1].replace('\n', ''))
    old_file.close()
    if max_dom > 0:
        new_file.write("&share\nmax_dom=" + str(max_dom) + ",\n")
        newline = 'start_date = '
        for val in start_date_list:
            newline = newline + ' ' + str(val)
        new_file.write(newline + '\n')
        newline = 'end_date = '
        for val in end_date_list:
            newline = newline + ' ' + str(val)
        new_file.write(newline + '\n')
        new_file.write("/\n\n")

    old_file = open(options.geogrid_info)
    for line in old_file:
        if 'parent_id_' in line:
            tmp = line.split('=')
            parent_id_list.append(tmp[1].replace('\n', ''))
        elif 'parent_grid_ratio_' in line:
            tmp = line.split('=')
            parent_grid_ratio_list.append(tmp[1].replace('\n', ''))
        elif 'i_parent_start_' in line:
            tmp = line.split('=')
            i_parent_start_list.append(tmp[1].replace('\n', ''))
        elif 'j_parent_start_' in line:
            tmp = line.split('=')
            j_parent_start_list.append(tmp[1].replace('\n', ''))
        elif 'e_we_' in line:
            tmp = line.split('=')
            e_we_list.append(tmp[1].replace('\n', ''))
        elif 'e_sn_' in line:
            tmp = line.split('=')
            e_sn_list.append(tmp[1].replace('\n', ''))
        elif 'geog_data_res_' in line:
            tmp = line.split('=')
            geog_data_res_list.append(tmp[1].replace('\n', ''))
        elif 'start_date_' in line:
            tmp = line.split('=')
        elif 'end_date' in line:
            tmp = line.split('=')
        else:
            tmp = line.replace('\n', '')
            if tmp.rstrip():
                new_file.write(tmp.strip() + '\n')

    old_file.close()
    newline = 'parent_id = '
    for val in parent_id_list:
        newline = newline + ' ' + str(val)
    new_file.write(newline + '\n')
    newline = 'parent_grid_ratio = '
    for val in parent_grid_ratio_list:
        newline = newline + ' ' + str(val)
    new_file.write(newline + '\n')
    newline = 'i_parent_start = '
    for val in i_parent_start_list:
        newline = newline + ' ' + str(val)
    new_file.write(newline + '\n')
    newline = 'j_parent_start = '
    for val in j_parent_start_list:
        newline = newline + ' ' + str(val)
    new_file.write(newline + '\n')
    newline = 'e_we = '
    for val in e_we_list:
        newline = newline + ' ' + str(val)
    new_file.write(newline + '\n')
    newline = 'e_sn = '
    for val in e_sn_list:
        newline = newline + ' ' + str(val)
    new_file.write(newline + '\n')
    newline = 'geog_data_res = '
    for val in geog_data_res_list:
        newline = newline + ' ' + str(val)
    new_file.write(newline + '\n')
    # end namelist
    new_file.write('/\n')
    # close temp file
    new_file.close()


if __name__ == "__main__":
    main()
