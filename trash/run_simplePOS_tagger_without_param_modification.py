import argparse
import os
from bin.model_calc import ModelCalculator
from bin.simple_pos_tagger import SimpleTagger
from bin.compare_tagged_output import compare_tweet_files


parser = argparse.ArgumentParser()

parser.add_argument("-m", dest="model_params_filename", help="File to load Model Params from")
parser.add_argument("-d", dest="testdata_filename", help="File to load untagged test data from")
parser.add_argument("-o", dest="output_filename", help="File to write output to")
parser.add_argument("-g", dest="gold_filename", help="File to reference when calculating match percentage")

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
  output_filename = 'dev.modSP.out'


if args.gold_filename is not None:
  gold_filename = args.gold_filename
else:
  gold_filename = os.path.join('data', 'dev.out')



model = ModelCalculator.init_from_params_file(model_params_filename)

simple_tagger = SimpleTagger(model.e_params, None, None, testdata_filename, output_filename, None)
simple_tagger.run_simple_tagger()


compare_tweet_files(output_filename, gold_filename)

