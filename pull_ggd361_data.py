import codecs
import csv
import datetime as dt
import getopt
import re
import sys

depths_seen = []
data_rows = []

def parse_date_and_time(row):
    datetime_regex = re.compile('\d{8}T\d{4}')
    date_and_time = datetime_regex.search(row)
    return date_and_time.group()

def parse_depth(row):
    depth_regex = re.compile('\d\d_CM')
    depth = depth_regex.search(row)
    if depth:
        if depth.group() not in depths_seen:
            depths_seen.append(depth.group())
        return depth.group()
    else:
        return depth

def parse_value(row):
    value_regex = re.compile(r'-?\d+\.\d+')
    value = value_regex.search(row)
    return value.group()

def parse_row(row):
    """ Pull date, time, depth, and data value from row. """
    date_and_time = parse_date_and_time(row)
    depth = parse_depth(row)
    value = parse_value(row)
    return [date_and_time, depth, value]

def pull_data(raw_file, out_file):
    """ Pull data fields out of raw data file. """
    print 'raw file = ', raw_file
    ifile = codecs.open(raw_file, 'r', encoding='utf_16_le')
    print 'out file = ', out_file
    ofile = open(out_file, 'w')
    writer = csv.writer(ofile, delimiter=',', quoting=csv.QUOTE_NONE)

    # for row in reader:
    for row in ifile:
        data_row = parse_row(row)
        data_rows.append(data_row)
    for a_row in data_rows:
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
    for opt, arg in opts:
        if opt == '-h':
            print 'pull_ggd361_data.py -i  <GGD361 raw data file> -o <CSV output file>'
            sys.exit()
        elif opt in ("-i", "--ggd361_raw_file"):
            raw_file = arg
        elif opt in ("-o", "--ggd361_data_file"):
            data_file = arg
    return (raw_file, data_file)


if __name__ == '__main__':
    (ggd361_raw_file, ggd361_data_file) = parse_arguments(sys.argv[1:])

    pull_data(raw_file=ggd361_raw_file,
              out_file=ggd361_data_file)
