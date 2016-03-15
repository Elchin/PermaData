""" Does multi column sort of CSV file. """

import ast
import csv
import datetime as dt
import getopt
import sys

gtnp_date_time_format = '%Y-%m-%d %H:%M'
date_time_index = None

def cast_to_datetime(dt_str):
    """
    Convert string to a datetime object.
    :param int_str: string to convert to a datetime object
    :return: datetime object
    """
    date_time = None
    try:
        date_time = dt.datetime.strptime(dt_str, gtnp_date_time_format)
    except ValueError as error:
        print error
    return date_time

def cast_to_integer(int_str):
    """
    Convert string to an integer.
    :param int_str: string to convert to an integer
    :return: integer number
    """
    return int(float(int_str))

def cast_to_real(real_str):
    """
    Convert string to a real.
    :param real_str: string to convert to a real
    :return: real number
    """
    return float(real_str)

def create_typed_row(row, column_list):
    """
    Make sure rows to be sorted by are in sortable form.
    :param row: CSV row
    :param column_list: list of sort by column tuples (index, type)
    :return: a row of typed values
    """
    global date_time_index
    row_list = list(row)
    for index, type in column_list:
        if type == 'dt':
            date_time_index = index
            row_list[index] = cast_to_datetime(row_list[index])
        elif type == 'integer':
            row_list[index] = cast_to_integer(row_list[index])
        elif type == 'real':
            row_list[index] = cast_to_real(row_list[index])
    return tuple(row_list)

def sort_by_columns(in_file, out_file, column_list):
    """
    Takes a list of columns to sort by in ascending order.
    :param in_file: CSV file to sort
    :param out_file: sorted CSV file
    :param column_list: list of tuples (index, type) describing sort columns
    """
    sorted_writer = csv.writer(open(out_file, 'w'), quotechar="'", quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n')
    header_row = None
    sorted_data = []
    with open(in_file, 'rb') as csvfile:
        unsorted_reader = csv.reader(csvfile, delimiter=',')
        csv_data = []
        ind = 0
        for row in unsorted_reader:
            row = [col_val.strip() for col_val in row]
            if ind > 0:
                typed_row = create_typed_row(row, column_list)
                csv_data.append(typed_row)
            else:
                header_row = row
            ind += 1
        for index, type in reversed(column_list):
            sorted_data = sorted(csv_data, key=lambda sort_by: sort_by[index])

    sorted_writer.writerow(header_row)
    for sorted_row in sorted_data:
        if date_time_index:
            row_list = list(sorted_row)
            row_list[date_time_index] = row_list[date_time_index].strftime(gtnp_date_time_format)
            sorted_row = tuple(row_list)
        sorted_writer.writerow(sorted_row)

def parse_arguments(argv):
    """ Parse the command line arguments and return them. """
    in_file = None
    out_file = None
    column_list = None
    try:
        opts, args = getopt.getopt(argv,"hi:o:l:",["in_file=","out_file=","column_list="])
    except getopt.GetoptError:
        print 'sort_by_columns.py -i <CSV input file> -o <CSV output file> -l <list of columns to sort by>'
        sys.exit(2)

    found_in_file = False
    found_out_file = False
    found_column_list = False
    for opt, arg in opts:
        if opt == '-h':
            print 'sort_by_columns.py -i <CSV input file> -o <CSV output file> -l <list of columns to sort by>'
            sys.exit()
        elif opt in ("-i", "--in_file"):
            found_in_file = True
            in_file = arg
        elif opt in ("-o", "--out_file"):
            found_out_file = True
            out_file = arg
        elif opt in ("-l", "--column_list"):
            found_column_list = True
            column_list = ast.literal_eval(arg)
    if not found_in_file:
        print "Input file '-i' argument required."
        sys.exit(2)
    if not found_out_file:
        print "Output file '-o' argument required."
        sys.exit(2)
    if not found_column_list:
        print "Ordered list of columns to sort by '-l' argument required."
        sys.exit(2)
    return in_file, out_file, column_list

if __name__ == '__main__':
    (in_file, out_file, column_list) = parse_arguments(sys.argv[1:])

    sort_by_columns(in_file, out_file, column_list)
