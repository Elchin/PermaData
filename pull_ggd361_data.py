""" Reader for data files from dataset GGD361 (Soil Temperatures at
    Climatological Stations in Centre d'Etudes Nordiques, Quebec, Canada """
import codecs
import csv
import getopt
import re
import sys

depths_seen = []
data_rows = [('Station', 'date:time', 'Depth', 'Temperature')]

def parse_substation_code(row):
    """ Extract substation code from data row. """
    substation_regex = re.compile(r'\d{4,5}')
    data_code = substation_regex.search(row)
    return row[data_code.end():data_code.end() + 7]

def parse_date_and_time(row):
    """ Extract date/time field from data row. """
    datetime_regex = re.compile(r'\d{8}T\d{4}')
    date_and_time = datetime_regex.search(row)
    return date_and_time.group()

def parse_depth(row):
    """ Extract depth field from data row. """
    depth_regex = re.compile(r'\d+_CM')
    depth = depth_regex.search(row)
    if depth:
        depth = depth.group().replace('_CM', '.0')
        if depth not in depths_seen:
            depths_seen.append(depth)
    return depth

def parse_value(row):
    """ Extract temperature field from data row. """
    value_regex = re.compile(r'-?\d+\.\d+')
    value = value_regex.search(row)
    return value.group()

def parse_row(row):
    """ Pull date, time, depth, and data value from row. """
    station_id = parse_substation_code(row)
    date_and_time = parse_date_and_time(row)
    depth = parse_depth(row)
    value = parse_value(row)
    return [station_id, date_and_time, depth, value]

def pull_data(raw_file, out_file):
    """ Pull data fields out of raw data file. """
    print 'raw file = ', raw_file
    ifile = codecs.open(raw_file, 'r', encoding='utf_16_le')
    print 'out file = ', out_file
    ofile = open(out_file, 'w')
    writer = csv.writer(ofile, delimiter=',', quoting=csv.QUOTE_NONE)

    for row in ifile:
        data_row = parse_row(row)
        data_rows.append(data_row)

    for a_row in data_rows:
        if not a_row[2]:
            if len(depths_seen) is 1:
                a_row = (a_row[0], a_row[1], depths_seen[0], a_row[3])
            else:
                print "Ambiguous depth for: {0} {1} {2}\nThis row will not be " \
                      "written to csv file.".format(a_row[0], a_row[1], a_row[3])
                a_row = None
        if a_row:
            writer.writerow(a_row)

    ifile.close()
    ofile.close()

def parse_arguments(argv):
    """ Parse the command line arguments and return them. """
    raw_file = None
    data_file = None
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ggd361_raw_file=","ggd361_data_file="])
    except getopt.GetoptError:
        print 'pull_ggd361_data.py -i <GGD361 raw data file> -o <CSV output file>'
        sys.exit(2)

    found_in_file = False
    found_out_file = False
    for opt, arg in opts:
        if opt == '-h':
            print 'pull_ggd361_data.py -i  <GGD361 raw data file> -o <CSV output file>'
            sys.exit()
        elif opt in ("-i", "--ggd361_raw_file"):
            found_in_file = True
            raw_file = arg
        elif opt in ("-o", "--ggd361_data_file"):
            found_out_file = True
            data_file = arg
    if not found_in_file:
        print "Input file '-i' argument required."
        sys.exit(2)
    if not found_out_file:
        print "Output file '-o' argument required."
        sys.exit(2)
    return (raw_file, data_file)


if __name__ == '__main__':
    (ggd361_raw_file, ggd361_data_file) = parse_arguments(sys.argv[1:])

    pull_data(raw_file=ggd361_raw_file,
              out_file=ggd361_data_file)
