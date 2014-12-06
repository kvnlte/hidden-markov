import argparse
from model_calc import ModelCalculator
from simple_pos_tagger import SimpleTagger


parser = argparse.ArgumentParser()

parser.add_argument("-m", dest="model_params_filename", help="File to load Model Params from")
parser.add_argument("-d", dest="testdata_filename", help="File to load untagged test data from")
parser.add_argument("-o", dest="output_filename", help="File to write output to")

args = parser.parse_args()

model = ModelCalculator.init_from_params_file(args.model_params_filename)

simple_tagger = SimpleTagger(model.e_params, None, None, args.testdata_filename, args.output_filename, None)
simple_tagger.run_simple_tagger()
