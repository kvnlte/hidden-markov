import os
import argparse
from bin.model_calc import ModelCalculator
from bin.viterbi_algo import ViterbiAlgorithm
from bin.compare_tagged_output import compare_tweet_files

parser = argparse.ArgumentParser()

parser.add_argument("-t", dest="training_data_filename", type=str, help="Training Data Filename")
parser.add_argument("-m", dest="model_params_filename", help="File to load Model Params from")
parser.add_argument("-d", dest="testdata_filename", help="File to load untagged test data from")
parser.add_argument("-o", dest="output_filename", help="File to write output to")
parser.add_argument("-g", dest="gold_filename", help="File to treat as gold standard")

args = parser.parse_args()



if args.training_data_filename is not None:
  training_data_filename = args.training_data_filename
else:
  training_data_filename = os.path.join('data', 'train')


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
  output_filename = 'dev.vitalgo.out'


if args.gold_filename is not None:
  gold_filename = args.gold_filename
else:
  gold_filename = os.path.join('data', 'dev.out')


model = ModelCalculator(training_data_filename)
model.load_test_file(testdata_filename)
model.init_model_params()

model.save_model_params(model_params_filename)

viterbi = ViterbiAlgorithm(model)
viterbi.tag_all_tests()

viterbi.save_tagged_tests(output_filename)

compare_tweet_files(output_filename, gold_filename)

