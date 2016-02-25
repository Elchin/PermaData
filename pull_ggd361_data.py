import argparse as ap
import codecs
import csv
import datetime as dt
import re

depths_seen = []
data_rows = []

def parse_date_and_time(row):
    datetime_regex = re.compile('\d{8}T\d{4}')
    date_and_time = datetime_regex.search(row)
    print date_and_time.group()
    return date_and_time.group()

def parse_depth(row):
    depth_regex = re.compile('\d\d_CM')
    depth = depth_regex.search(row)
    if depth:
        if depth.group() not in depths_seen:
            depths_seen.append(depth.group())
        print depth.group()
        return depth.group()
    else:
        return depth

def parse_value(row):
    value_regex = re.compile(r'-?\d+\.\d+')
    value = value_regex.search(row)
    print value.group()
    return value.group()

def parse_row(row):
    """ Pull date, time, depth, and data value from row. """
    print row
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
        print data_row
        data_rows.append(data_row)
    for a_row in data_rows:
        writer.writerow(a_row)

    ifile.close()
    ofile.close()

def parse_arguments():
    """ Parse the command line arguments and return them. """
    parser = ap.ArgumentParser()
    parser.add_argument('ggd361_raw_file', help='The GGD361 raw data file from'
                        ' which to pull data.')
    parser.add_argument('ggd361_data_file', help='A CSV files containing the'
                        ' date/time (YYYY-MM-DD hh:mm), depth, and measurement'
                        ' value.')
    return parser.parse_args()


if __name__ == '__main__':
    parsed_args = parse_arguments()

    pull_data(raw_file=parsed_args.ggd361_raw_file,
              out_file=parsed_args.ggd361_data_file)
