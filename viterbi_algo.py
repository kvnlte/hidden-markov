import sys
import argparse
from model_calc import ModelCalculator


class ViterbiAlgorithm:

    def __init__(self, model_calculator):
        if not isinstance(model_calculator, ModelCalculator):
            raise TypeError("Expected ModelCalculator instance.")
        elif model_calculator.e_params is None or model_calculator.q_params is None:
            raise RuntimeError("Model parameters not initialized in ModelCalculator instance")
        elif model_calculator.test_data is None:
            raise RuntimeError("Test Data not loaded in ModelCalculator instance")

        self.model = model_calculator
        self.test_sentences = self.model.test_data.sentence_list

        self.e_params = self.model.e_params
        self.q_params = self.model.q_params
        self.tags = self.model.tags_seen  # expected to exclude '*' and 'STOP'

        self.tagged_test_sentences = None


    def tag_all_tests(self):
        self.tagged_test_sentences = []
        for sentence in self.test_sentences:
            tagged_sentence = self.tag_sentence(sentence)
            self.tagged_test_sentences.append(tagged_sentence)


    def save_tagged_tests(self, output_filename):
        output_file = open(output_filename, 'w')

        for sentence in self.tagged_test_sentences:
            for token in sentence:
                output_file.write("%s\t%s\n" % (token[0], token[1]))
            output_file.write('\n')

        output_file.close()

    def tag_sentence(self, sentence):
        tag_sequence = self.generate_tag_sequence(sentence)
        sequence_length = len(sentence)
        if sequence_length != len(tag_sequence):
            error_msg = "generate_tag_sequence() produced invalid result\n"
            error_msg += "length of sentence: %d\n" % sequence_length
            error_msg += "length of output: %d\n" % len(tag_sequence)
            raise RuntimeError(error_msg)

        tagged_sentence = [(sentence[i][0], tag_sequence[i]) for i in range(sequence_length)]

        return tuple(tagged_sentence)


    def generate_tag_sequence(self, sentence):
        # IMPORTANT: sentence should come from a TweetTokenizer instance,
        # and is not expected to contain '*' and 'STOP' tags

        graph = self.__generate_graph(sentence)

        sentence_buffer = list(sentence)

        # Begin Backtracing

        reversed_tag_sequence = ['STOP']
        target_score = graph.pop().keys()[0]  # score at 'STOP' tag

        while len(graph) > 0:
            sequence_count = len(reversed_tag_sequence)
            last_section = graph.pop()
            curr_tag = reversed_tag_sequence[-1]

            if curr_tag == 'STOP':
                curr_word = None
            else:
                curr_word = sentence_buffer.pop()[0]

            e_param = self.__find_e_param(curr_word, curr_tag)

            for curr_score in last_section:  # cycle through scores in last section
                curr_score_tag = last_section[curr_score]  # find tag corresponding to tag_score

                q_param = self.__find_q_param(curr_tag, curr_score_tag)

                est_score = curr_score * e_param * q_param  # calculate score if current score is used

                if est_score == target_score:  # curr_score corresponds to best tag
                    reversed_tag_sequence.append(curr_score_tag)
                    target_score = curr_score  # set next target score to best tag's score
                    break

            if sequence_count == len(reversed_tag_sequence):
                print "No corresponding score found."
                print "Current sequence progress:"
                print reversed_tag_sequence[::-1]
                raise RuntimeError('No corresponding score found')

        reversed_tag_sequence.remove('STOP')
        return reversed_tag_sequence[::-1]


    #### 'private' methods ####

    def __find_e_param(self, word, tag):
        if tag == "STOP":
            e_param = 1
        else:
            try:
                e_param = self.e_params[(word, tag)]
            except KeyError:
                e_param = 0  # emission does not occur in the training set

        return e_param

    def __find_q_param(self, curr_tag, prev_tag):
        try:
            q_param = self.q_params[(curr_tag, prev_tag)]
        except KeyError:  # transition does not occur in the training set
            q_param = 0

        return q_param


    def __calc_node_score(self, prev_section, curr_tag, curr_word=None):
        best_score = 0

        e_param = self.__find_e_param(curr_word, curr_tag)
        if e_param == 0:  # emission does not occur in the training set
            return 0

        for prev_score in prev_section:
            prev_tag = prev_section[prev_score]

            q_param = self.__find_q_param(curr_tag, prev_tag)

            curr_score = prev_score * e_param * q_param

            if curr_score > best_score:
                best_score = curr_score

        return best_score


    def __generate_graph(self, sentence):

        graph = []

        prev_section = {1: '*'}  # score for first tag '*': tag name '*'

        for token in sentence:
            curr_word = token[0]
            curr_section = {}

            for tag in self.tags:
                tag_score = self.__calc_node_score(prev_section, tag, curr_word)
                curr_section[tag_score] = tag

            graph.append(curr_section)
            prev_section = curr_section

        last_section = {self.__calc_node_score(prev_section, 'STOP'): 'STOP'}
        graph.append(last_section)

        return graph

#### End of ViterbiAlgorithm declaration #####


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", dest="training_data_filename", type=str, help="Training Data Filename")
    parser.add_argument("-d", dest="test_data_filename", type=str, help="Testing Data Filename")
    parser.add_argument("-m", dest="model_params_filename", type=str, help="Model Params Output Filename")
    parser.add_argument("-o", dest="output_filename", type=str, help="Output File")

    args = parser.parse_args()

    print "\n\n---- Processing file data ----\n"
    print "Training File: %s" % args.training_data_filename
    print "Test Data File: %s" % args.test_data_filename

    model = ModelCalculator(args.training_data_filename)
    model.load_test_file(args.test_data_filename)
    model.init_model_params()

    print "\nSaving new model_params file: %s\n" % args.model_params_filename

    model.save_model_params(args.model_params_filename)

    viterbi = ViterbiAlgorithm(model)

    print "\n ---- Running Viterbi Algorithm ----\n"

    viterbi.tag_all_tests()

    print "Saved tagged output file to: %s" % args.output_filename
    viterbi.save_tagged_tests(args.output_filename)

