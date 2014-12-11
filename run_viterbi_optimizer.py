import sys
import os
from collections import Counter
import argparse
import csv

from bin.raw_parser import TrgDataParser
from bin.simple_pos_tagger import SimpleTagger
from bin.viterbi_optimizer import ViterbiOptimizer
from bin.compare_tagged_output import compare_tweet_files
from bin.model_calc import ModelCalculator

sys.stdout.write("\n\n----- Beginning Parse -----\n\n")

parser = argparse.ArgumentParser()

parser.add_argument("-i", dest='trg_set_filename', type=str, help="training data file")
parser.add_argument("-o", dest='count_data_filename', type=str, help="count data file")
parser.add_argument("-p", dest='model_params_filename', type=str, help="model params data file")
parser.add_argument("-ti", dest='file_in', type=str, help="test data file without tags")
parser.add_argument("-to", dest='file_out_p', type=str, help="test data file with tags, phase 2")
parser.add_argument("-g", dest='file_gold', type=str, help="test data file with gold standard tags")
parser.add_argument("-c", dest='compare', help="Flag to decide whether or not to compare", action="store_true")

args = parser.parse_args()


if args.trg_set_filename is not None:
  trg_set_filename = args.trg_set_filename
else:
  trg_set_filename = os.path.join('data', 'pptrain')


if args.count_data_filename is not None:
  count_data_filename = args.count_data_filename
else:
  count_data_filename = 'eval_trgdata.csv'


if args.model_params_filename is not None:
  model_params_filename = args.model_params_filename
else:
  model_params_filename = 'model_params.csv'


if args.file_in is not None:
  file_in = args.file_in
else:
  file_in = os.path.join('data', 'ppdev.in')


if args.file_out_p is not None:
  file_out_p = args.file_out_p
else:
  file_out_p = 'dev.p2.out'


if args.file_gold is not None:
  file_gold = args.file_gold
else:
  file_gold = os.path.join('data', 'ppdev.out')





raw_data_filename = trg_set_filename
count_data_filename = count_data_filename
model_params_filename = model_params_filename

sys.stdout.write("Specified Traing Data File: %s\n" % raw_data_filename)
sys.stdout.write("Specified Count Data File: %s\n" % count_data_filename)
sys.stdout.write("Specified Model Params File: %s\n" % model_params_filename)



model = ModelCalculator(raw_data_filename)
model.load_test_file(file_in)
model.init_model_params()


train_q_params = model.q_params
train_e_params = model.e_params
#file_in = testdata_filename
#file_out = output_filename
#file_gold = os.path.join('data', 'dev.out')
states = model.tags_seen + ['*', 'STOP']

file_out_p=file_out_p
final_viterbi=ViterbiOptimizer(train_q_params,train_e_params,file_in,file_out_p,file_gold,states)
final_viterbi.tokenize_input()
final_viterbi.tokenize_gold()
final_viterbi.run()
#print final_viterbi.start_params

if args.compare:
    compare_tweet_files(file_out_p, file_gold)

sys.stdout.write("\n\n----- Completed Parse -----\n\n")
