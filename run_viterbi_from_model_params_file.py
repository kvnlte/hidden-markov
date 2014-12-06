import argparse
from model_calc import ModelCalculator
from viterbi_algo import ViterbiAlgorithm

parser = argparse.ArgumentParser()

parser.add_argument("-m", dest="model_params_filename", help="File to load Model Params from")
parser.add_argument("-sp", dest="use_simplePOS", action="store", help="Flag to indicate whether to use simplePOS emission params")
parser.add_argument("-d", dest="testdata_filename", help="File to load untagged test data from")
parser.add_argument("-o", dest="output_filename", help="File to write output to")

args = parser.parse_args()



model = ModelCalculator.init_from_params_file(args.model_params_filename)

if args.use_simplePOS:
    model.update_emissions_with_SimpleTagger_method(args.testdata_filename)

model.load_test_file(args.testdata_filename)

viterbi = ViterbiAlgorithm(model)

viterbi.tag_all_tests()
viterbi.save_tagged_tests(args.output_filename)
