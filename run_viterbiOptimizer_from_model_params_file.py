import argparse
from model_calc import ModelCalculator
from viterbi_optimizer import ViterbiOptimizer

parser = argparse.ArgumentParser()

parser.add_argument("-m", dest="model_params_filename", help="File to load Model Params from")
parser.add_argument("-sp", dest="use_simplePOS", action="store_true", help="Flag to indicate whether to use simplePOS emission params")
parser.add_argument("-d", dest="testdata_filename", help="File to load untagged test data from")
parser.add_argument("-o", dest="output_filename", help="File to write output to")

args = parser.parse_args()



model = ModelCalculator.init_from_params_file(args.model_params_filename)

if args.use_simplePOS:
    model.update_emissions_with_SimpleTagger_method(args.testdata_filename)

model.load_test_file(args.testdata_filename)

q_params = model.q_params
e_params = model.e_params
file_in = args.testdata_filename
file_out = args.output_filename
file_gold = 'dev.out'
states = model.tags_seen + ['*', 'STOP']

viterbi = ViterbiOptimizer(q_params, e_params, file_in, file_out, file_gold, states)

viterbi.tokenize_input()
viterbi.tokenize_gold()
viterbi.run()

viterbi.compare_accuracy()

