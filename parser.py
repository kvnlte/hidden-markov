import sys
from collections import Counter
import argparse
import csv


class TweetPOSParser:

    def __init__(self, input_filename, output_filename):
        self.input_filename = input_filename
        self.output_filename = output_filename

        self.e_data_counter = Counter()
        self.q_data_counter = Counter()
        self.tag_counter = Counter()

        self.__data_loaded = False

    def load_data(self):

        if self.__data_loaded:
            return None         # only load data once

        input_file = open(self.input_filename)

        prev_tag = 'STOP'


        for line in input_file:
            line = line.strip()   # remove trailing whitespace

            terms = line.split('\t')

            if terms[0] == '':    # end of tweet
                curr_word = ''
                curr_tag = 'STOP'

            else:     # terms represents a word in the tweet
                curr_word = terms[0]
                curr_tag = terms[1]

            if prev_tag == 'STOP':
                if curr_tag == 'STOP':    # empty line preceded by empty line
                    continue
                else:          # first line in file / first line of new tweet
                    prev_tag = '*'
                    self.tag_counter[prev_tag] += 1


            self.__increm_counters(prev_tag, curr_tag, curr_word)

            prev_tag = curr_tag
            # print curr_word, curr_tag


        ##
        ## end of file reached

        if prev_tag != 'STOP':
            curr_word = ''
            curr_tag = 'STOP'

            self.__increm_counters(prev_tag, curr_tag, curr_word)


        # print_counter_data(self.e_data_counter, "e_data_counter")
        # print_counter_data(self.q_data_counter, "q_data_counter")
        print_counter_data(self.tag_counter, "tag_counter")

        self.__data_loaded = True
        input_file.close()

    def __increm_counters(self, prev_tag, curr_tag, curr_word):
        x_y = (curr_word, curr_tag)
        y_yp = (curr_tag, prev_tag)

        # to increment count( x given y )
        self.e_data_counter[x_y] += 1

        # to increment count( y(i) given y(i-1) )
        self.q_data_counter[y_yp] += 1

        # to increment count( y )
        self.tag_counter[curr_tag] += 1


    def save_data(self, output_filename=None):
        if output_filename == None:
            output_filename = self.output_filename

        with open(output_filename, 'wb') as csvfile:
            data_writer = csv.writer(csvfile)
            self.__write_csv_batch(self.e_data_counter, 'e', data_writer)
            self.__write_csv_batch(self.q_data_counter, 'q', data_writer)
            self.__write_csv_batch(self.tag_counter, '', data_writer)


    def __write_csv_batch(self, counter, t_type, csv_writer):
        for elem in counter:
            if t_type != '':        # elem/data is either count( x given y ) or count ( y(i) given y(i-1) )
                first_t = elem[0]
                second_t = elem[1]
            else:                   # elem/data is count( y )
                first_t = elem
                second_t = ''
            count = counter[elem]

            csv_writer.writerow([t_type, first_t, second_t, count])

def print_counter_data(counter, counter_name):
    assert isinstance(counter, Counter)

    sys.stdout.write("\n--- printing data for %s\n\n" % counter_name)
    for elem in counter:
        print elem, counter[elem]

    sys.stdout.write("--- done printing\n\n")



if __name__ == "__main__":
    sys.stdout.write("\n\n----- Beginning Parse -----\n\n")

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", type=str, help="input data file")
    parser.add_argument("-o", type=str, help="output data file")

    args = parser.parse_args()

    sys.stdout.write("Specified Input File: %s\n" % args.i)
    sys.stdout.write("Specified Output File: %s\n" % args.o)

    tweet_parser = TweetPOSParser(args.i, args.o)
    tweet_parser.load_data()
    tweet_parser.save_data()

    sys.stdout.write("\n\n----- Completed Parse -----\n\n")
