""" String replace for column values. """
import csv
import getopt
import sys

def replace_text(ggd361_csv, out_file, column, to_replace, with_replace):
    """
    Replace text within field with new text.
    :param ggd361_csv: input CSV file
    :param out_file: output CSV file
    :param column: name of column of string fields in CSV input file header
    :param to_replace: substring within field to be replaced
    :param with_replace: substring to replace to_replace substring
    """
    ofile = open(out_file, 'w')
    writer = csv.writer(ofile, delimiter=',', quoting=csv.QUOTE_NONE, lineterminator='\n')

    csv_data = []
    field_names = None
    is_header = True
    col_ind = None
    with open(ggd361_csv) as csv_values:
        reader = csv.reader(csv_values, delimiter=',', quoting=csv.QUOTE_NONE)
        for row in reader:
            if is_header:
                col_names = [field.replace('\'', '') for field in row]
                try:
                    col_ind = col_names.index(column)
                except ValueError:
                    print "Cannot find column {0} in CSV file.".format(column)
                    sys.exit(2)
                is_header = False
            else:
                field = row[col_ind].replace('\'', '')
                new_field = field.replace(to_replace, with_replace)
                row[col_ind] = '\'' + new_field + '\''

            writer.writerow(row)
    ofile.close()

def parse_arguments(argv):
    """ Parse the command line arguments and return them. """
    ggd361_csv = None
    out_file = None
    column = None
    to_replace = None
    with_replace = None

    try:
        opts, args = getopt.getopt(argv,"hi:o:c:t:w:",["ggd361_csv=","out_file=","column=","to_replace=","with_replace="])
    except getopt.GetoptError:
        print 'replace_text.py -i <GGD361 CSV file> -o <CSV output file> -c <column name of text field> -t <text in field to replace> -w <replacement text>'
        sys.exit(2)

    found_in_file = False
    found_out_file = False
    found_column = False
    found_to_replace = False
    found_with_replace = False
    for opt, arg in opts:
        if opt == '-h':
            print 'replace_text.py -i <GGD361 CSV file> -o <CSV output file> -c <column name of text field> -t <text in field to replace> -w <replacement text>'
            sys.exit()
        elif opt in ("-i", "--ggd361_csv"):
            found_in_file = True
            ggd361_csv = arg
        elif opt in ("-o", "--out_file"):
            found_out_file = True
            out_file = arg
        elif opt in ("-c", "--column"):
            found_column = True
            column = arg
        elif opt in ("-t", "--to_replace"):
            found_to_replace = True
            to_replace = arg
        elif opt in ("-w", "--with_replace"):
            found_with_replace = True
            with_replace = arg
    if not found_in_file:
        print "Input file '-i' argument required."
        sys.exit(2)
    if not found_out_file:
        print "Output file '-o' argument required."
        sys.exit(2)
    if not found_column:
        print "Column name of text field '-c' argument required."
        sys.exit(2)
    if not found_to_replace:
        print "Text within field to replace '-t' argument required."
        sys.exit(2)
    if not found_with_replace:
        print "Replacement text '-w' argument required."
        sys.exit(2)
    return (ggd361_csv, out_file, column, to_replace, with_replace)


if __name__ == '__main__':
    (ggd361_csv, output_csv, column, to_replace, with_replace) = parse_arguments(sys.argv[1:])

    replace_text(ggd361_csv.strip(), output_csv.strip(), column.strip(), to_replace.strip(), with_replace.strip())
