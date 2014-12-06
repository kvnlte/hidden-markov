import sys
from collections import Counter
import argparse
import csv


class TrgDataParser:

    def __init__(self, raw_data_filename):
        self.raw_data_filename = raw_data_filename

        self.e_data_counter = Counter()     # keys will be tuples of the form (word, tag)
        self.q_data_counter = Counter()     # keys will by tuples of the form (tag_n, tag_n_minus_1)
        self.tag_counter = Counter()

        self.e_params = {}
        self.q_params = {}

        self.__data_loaded = False          # tracks if read_raw_data() has been called
        self.__params_generated = False     # tracks if generate_model_params() has been called

    def read_raw_data(self):
        """
        Processes the raw data file into count data,
        Stored in self.e_data_counter, self.q_data_counter and self.tag_counter as Counters.

        :return: None
        """

        if self.__data_loaded:
            return None         # only load data once

        input_file = open(self.raw_data_filename)

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


    def save_count_data(self, output_filename):
        """
        Saves the count data into a csv formatted file.
        read_raw_data() must be called before using this method.

        :param output_filename: String
        :return: None
        """

        with open(output_filename, 'wb') as csvfile:
            data_writer = csv.writer(csvfile)
            self.__write_count_batch(self.e_data_counter, 'e', data_writer)
            self.__write_count_batch(self.q_data_counter, 'q', data_writer)
            self.__write_count_batch(self.tag_counter, '', data_writer)


    def generate_model_params(self):
        """
        Calculates the emission and transmission parameters from the training set
        Using Maximum Likelihood Estimation (MLE).
        Parameters generated are stored in self.e_params and self.q_params as dictionaries.

        :return: None
        """
        if self.__params_generated:
            return None         # only generate model params once

        for emission in self.e_data_counter:    # generate emission parameters
            tag = emission[1]
            self.e_params[emission] = self.e_data_counter[emission] / float(self.tag_counter[tag])

        for transition in self.q_data_counter:  # generate transmission parameters
            prev_tag = transition[1]
            self.q_params[transition] = self.q_data_counter[transition] / float(self.tag_counter[prev_tag])


    def save_model_params(self, output_filename):
        """
        Saves generated model params into a cav formatted file.
        generate_model_params() must be called before using this method.

        :param output_filename: String
        :return: None
        """
        with open(output_filename, 'wb') as csvfile:
            params_writer = csv.writer(csvfile)
            for param in self.e_params:
                word = param[0]
                tag = param[1]
                e_value = self.e_params[param]

                params_writer.writerow(['e', word, tag, e_value])

            for param in self.q_params:
                tag = param[0]
                prev_tag = param[1]
                q_value = self.q_params[param]

                params_writer.writerow(['q', tag, prev_tag, q_value])


    def viterbi(self):
        

    @staticmethod
    def __write_count_batch(counter, t_type, csv_writer):
        for elem in counter:
            if t_type != '':        # elem/data is either count( x given y ) or count ( y(i) given y(i-1) )
                first_t = elem[0]
                second_t = elem[1]
            else:                   # elem/data is count( y )
                first_t = elem
                second_t = ''
            count = counter[elem]

            csv_writer.writerow([t_type, first_t, second_t, count])


## End of TweetParse declaration



def print_counter_data(counter, counter_name):
    assert isinstance(counter, Counter)

    sys.stdout.write("\n--- printing data for %s\n\n" % counter_name)
    for elem in counter:
        print elem, counter[elem]

    sys.stdout.write("--- done printing\n\n")



###############################################################################

if __name__ == "__main__":
    sys.stdout.write("\n\n----- Beginning Parse -----\n\n")

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", dest='trg_set_filename', type=str, help="training data file")
    parser.add_argument("-o", dest='count_data_filename', type=str, help="count data file")
    parser.add_argument("-p", dest='model_params_filename', type=str, help="model params data file")

    args = parser.parse_args()

    raw_data_filename = args.trg_set_filename
    count_data_filename = args.count_data_filename
    model_params_filename = args.model_params_filename

    sys.stdout.write("Specified Traing Data File: %s\n" % raw_data_filename)
    sys.stdout.write("Specified Count Data File: %s\n" % count_data_filename)
    sys.stdout.write("Specified Model Params File: %s\n" % model_params_filename)

    training_parser = TrgDataParser(raw_data_filename)
    training_parser.read_raw_data()
    training_parser.save_count_data(count_data_filename)
    training_parser.generate_model_params()
    training_parser.save_model_params(model_params_filename)

    sys.stdout.write("\n\n----- Completed Parse -----\n\n")
