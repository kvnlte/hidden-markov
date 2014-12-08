import simple_pos_tagger_util as util

class SimpleTagger:

    @classmethod
    def create_simple_tagger(cls, args):
        e_params, t_params = util.get_params(args)
        e_counts, t_counts, y_counts = util.get_counts(args)
        return SimpleTagger(e_params, e_counts, y_counts, args.i, args.o, args.g)

    def __init__(self, e_params, e_counts, y_counts, file_in, file_out, gold_out):
        self.emission_params = e_params
        self.emission_counts = e_counts
        self.y_counts = y_counts
        self.input = file_in
        self.output = file_out
        self.gold_output = gold_out

    def update_emission_parameters(self):
        print "\n----- Updating Emission Parameters -----"

        input_file = open(self.input)

        for line in input_file:
            current_word = line.strip()

            # skip blank words
            if current_word == "":
                continue

            new_word_encountered = True # default value

            for key in self.emission_params:
                if key[0] == current_word:
                    new_word_encountered = False
                    break

            if new_word_encountered:
                self.update_emission_params_for_seen_words()
                self.create_emission_params_for_new_words(current_word)

        input_file.close()

        print "----- Emission Parameters Updated -----"

    def update_emission_params_for_seen_words(self):
        for key in self.emission_params:
            y = key[1]
            previous_ep = self.emission_params[key]
            count_y = self.y_counts[y]

            # previous ep = count(y->x)/count(y)
            # therefore, new ep = count(y->x)/(count(y)+1)
            #                   = (count(y->x)/(count(y))*count(y)/(count(y)+1)
            #                   = previous_ep*count(y)/(count(y)+1)
            new_ep = previous_ep*count_y / (count_y+1)
            self.emission_params[key] = new_ep

    def create_emission_params_for_new_words(self, new_word):
        for y in self.y_counts:
            count_y = self.y_counts[y]
            new_ep = 1.0 / (count_y+1)
            new_key = (new_word, y)
            self.emission_params[new_key] = new_ep       
        
    def run_simple_tagger(self):
        print "\n----- Begin Tagging -----"

        input_file = open(self.input)
        output_file = open(self.output, 'w')
        output = []

        for line in input_file:
            current_word = line.strip()

            if current_word == "":
                output.append("")
                continue
            else:
                predicted_label = self.get_label_with_argmax(current_word)
                row = current_word + '\t' + predicted_label
                output.append(row)

        # assemble final output to be written to output file
        final_output = ""
        for row in output:
            final_output += row + '\n'

        output_file.write(final_output)
        output_file.close()
        input_file.close()
        print "----- Tagging Complete. Saved to %s -----\n" % self.output

    def get_label_with_argmax(self, word):
        argmax = 0
        corresponding_label = ""

        for key in self.emission_params:
            if key[0] == word:
                if argmax < self.emission_params[key]:
                    argmax = self.emission_params[key]
                    corresponding_label = key[1]
        
        return corresponding_label
    
    def check_accuracy(self):
        output_file = open(self.output, 'r')
        gold_output_file = open(self.gold_output, 'r')

        correct = 0
        total = 0

        for a in output_file:
            a = a.split('\t')
            b = gold_output_file.readline().split('\t')

            if (len(a) == 2):
                if a[1] == b[1]:
                    correct += 1
                total += 1

        percentage_accuracy = (float(correct) / total) * 100
        print "Accuracy: %.2f%%" % percentage_accuracy


if __name__ == "__main__":
    print "\n----- Beginning Simple POS Tagger -----\n"
    args = util.parse_arguments()

    tagger = SimpleTagger.create_simple_tagger(args)
    tagger.update_emission_parameters()
    tagger.run_simple_tagger()
    tagger.check_accuracy()
