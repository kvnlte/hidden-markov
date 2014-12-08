import argparse
import csv

def parse_arguments():
    parser = get_parser()
    args = parser.parse_args()
    print_file_names(args)
    return args

def get_parser():
    parser = argparse.ArgumentParser()
    add_args_to_parser(parser)
    return parser

def add_args_to_parser(parser):
    parser.add_argument(
        '-m', dest='m', help='file containing model parameters')
    parser.add_argument(
        '-e', dest='e', help='file containing evaluated training data')
    parser.add_argument(
        '-i', dest='i', help='file containing test data to be tagged')
    parser.add_argument(
        '-o', dest='o', help='output file to contain predicted tags')
    parser.add_argument(
        '-g', dest='g', help='file containing gold-standard outputs')

def print_file_names(args):
    print "File for Model Parameters: %s" % args.m
    print "File for Evaluated Training Data: %s" % args.e
    print "File to be Tagged: %s" % args.i
    print "File with Predicted Tags: %s" % args.o
    print "File Containing Gold-Standard Outputs: %s" % args.g

def get_params(args):
    emission_params = {}
    transmission_params = {}

    with open(args.m, 'rb') as f:
        csv_file_contents = csv.reader(f)
        for row in csv_file_contents:
            if row[0] == 'e':
                key = (row[1], row[2])
                value = row[3]
                emission_params[key] = float(value)
            else:
                key = (row[1], row[2])
                value = row[3]
                transmission_params[key] = float(value)
             
        return emission_params, transmission_params

def get_counts(args):
    emission_counts = {}
    transmission_counts = {}
    y_counts = {}

    with open(args.e, 'rb') as f:
        csv_file_contents = csv.reader(f)
        for row in csv_file_contents:
            if row[0] == 'e':
                key = (row[1], row[2])
                value = row[3]
                emission_counts[key] = int(value)
            elif row[0] == 'q':
                key = (row[1], row[2])
                value = row[3]
                transmission_counts[key] = int(value)
            else:
                key = row[1]
                value = row[3]
                y_counts[key] = int(value)

    return emission_counts, transmission_counts, y_counts
