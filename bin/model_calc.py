import csv
from collections import Counter
from raw_parser import TrgDataParser
from tokenizer import TweetTokenizer
from simple_pos_tagger import SimpleTagger

class ModelCalculator:

    def __init__(self, trgdata_filename, skip_parse = False):
        if not skip_parse:
            self.parser = TrgDataParser(trgdata_filename)
            self.parser.read_raw_data()

            self.tag_counter = self.parser.tag_counter
            self.tags_seen = self.tag_counter.keys()
            self.tags_seen.remove('*')
            self.tags_seen.remove('STOP')

            self.word_counter = self.parser.word_counter
            self.e_counts = self.parser.e_data_counter
            self.q_counts = self.parser.q_data_counter

        self.test_data = None     # TweetTokenizer instance assigned by load_test_file()
        self.e_params = None
        self.q_params = None

    def init_model_params_from_file(self, params_filename):
        print "\n---- initializing Model Params from %s ----\n" % params_filename
        self.e_params = {}
        self.q_params = {}

        with open(params_filename, 'r') as csvfile:
            data_reader = csv.reader(csvfile)

            for row in data_reader:
                param_key = (row[1], row[2])
                if row[0] == 'e':   # e_param
                    self.e_params[param_key] = float(row[3])
                else:               # q_param
                    self.q_params[param_key] = float(row[3])

        # count tags seen

        tag_counter = Counter()
        for word, tag in self.e_params:
            tag_counter[tag] += 1
        self.tags_seen = tag_counter.keys()
        self.tags_seen.remove('STOP')
        

    def update_emissions_with_SimpleTagger_method(self, test_filename):
        simple_tagger = SimpleTagger(self.e_params, None, self.tag_counter, test_filename, None, None)
        simple_tagger.update_emission_parameters()
        self.e_params = simple_tagger.emission_params


    def save_model_params(self, output_filename):
        parser = TrgDataParser(None)
        parser.e_params = self.e_params
        parser.q_params = self.q_params

        parser.save_model_params(output_filename)


    def load_test_file(self, test_filename):
        self.test_data = TweetTokenizer(test_filename)
        self.test_data.tokenize()


    def init_model_params(self):
        if self.test_data is None:
            raise RuntimeError("Run load_test_file() before init_model_params")

        self.__init_q_params()
        self.__amend_emission_counts()
        self.__init_e_params()


    #### 'private' methods ####

    def __init_q_params(self):
        self.q_params = {}
        for q in self.q_counts:
            prev_tag = q[1]
            self.q_params[q] = self.q_counts[q] / float(self.tag_counter[prev_tag])

    def __init_e_params(self):      # IMPORTANT: Only run this after __amend_emission_counts()
        self.e_params = {}
        for e in self.e_counts:
            tag = e[1]
            self.e_params[e] = self.e_counts[e] / float(self.tag_counter[tag])

    def __amend_emission_counts(self):      # IMPORTANT: Only run after load_test_file()
        trgwords_set = frozenset(self.parser.word_counter.keys())

        test_words = self.test_data.word_counter.keys()

        for word in test_words:
            if word not in trgwords_set:
                self.__add_emission_counts_for_new_word(word)
                self.__increment_tag_counts()

    def __add_emission_counts_for_new_word(self, word):
        for tag in self.tags_seen:
            self.e_counts[(word, tag)] += 1

    def __increment_tag_counts(self):
        for tag in self.tag_counter:
            self.tag_counter[tag] += 1


#### end of ModelCalculator declaration ####

