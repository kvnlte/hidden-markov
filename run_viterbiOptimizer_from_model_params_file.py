import os
import argparse
from bin.model_calc import ModelCalculator
from bin.viterbi_optimizer import ViterbiOptimizer
from bin.compare_tagged_output import compare_tweet_files

parser = argparse.ArgumentParser()

parser.add_argument("-m", dest="model_params_filename", help="File to load Model Params from")
parser.add_argument("-sp", dest="use_simplePOS", action="store_true", help="Flag to indicate whether to use simplePOS emission params")
parser.add_argument("-d", dest="testdata_filename", help="File to load untagged test data from")
parser.add_argument("-o", dest="output_filename", help="File to write output to")
parser.add_argument("-t", dest="traindata_filename", help="File to use as training data")

args = parser.parse_args()

if args.model_params_filename is not None:
  model_params_filename = args.model_params_filename
else:
  model_params_filename = 'model_params.csv'


if args.testdata_filename is not None:
  testdata_filename = args.testdata_filename
else:
  testdata_filename = os.path.join('data', 'dev.in')


if args.output_filename is not None:
  output_filename = args.output_filename
else:
  output_filename = 'dev.modvitopt.out'


if args.traindata_filename is not None:
  traindata_filename = args.traindata_filename
else:
  traindata_filename = os.path.join('data', 'train')





# model = ModelCalculator.init_from_params_file(model_params_filename)

if args.use_simplePOS:
    model = ModelCalculator(traindata_filename)
    model.init_model_params_from_file(model_params_filename)
    model.update_emissions_with_SimpleTagger_method(testdata_filename)
else:
    model = ModelCalculator(None, True)
    model.init_model_params_from_file(model_params_filename)


q_params = model.q_params
e_params = model.e_params
file_in = testdata_filename
file_out = output_filename
file_gold = os.path.join('data', 'dev.out')
states = model.tags_seen + ['*', 'STOP']

viterbi = ViterbiOptimizer(q_params, e_params, file_in, file_out, file_gold, states)

viterbi.tokenize_input()
viterbi.tokenize_gold()
viterbi.run()

compare_tweet_files(output_filename, file_gold)
