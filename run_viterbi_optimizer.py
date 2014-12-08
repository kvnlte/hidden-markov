import sys
import os
from collections import Counter
import argparse
import csv

from bin.raw_parser import TrgDataParser
from bin.simple_pos_tagger import SimpleTagger
from bin.viterbi_optimizer import ViterbiOptimizer
from bin.compare_tagged_output import compare_tweet_files


sys.stdout.write("\n\n----- Beginning Parse -----\n\n")

parser = argparse.ArgumentParser()

parser.add_argument("-i", dest='trg_set_filename', type=str, help="training data file")
parser.add_argument("-o", dest='count_data_filename', type=str, help="count data file")
parser.add_argument("-p", dest='model_params_filename', type=str, help="model params data file")
parser.add_argument("-ti", dest='file_in', type=str, help="test data file without tags")
parser.add_argument("-to1", dest='file_out_p1', type=str, help="test data file with tags, phase 1")
parser.add_argument("-to2", dest='file_out_p2', type=str, help="test data file with tags, phase 2")
parser.add_argument("-g", dest='file_gold', type=str, help="test data file with gold standard tags")

args = parser.parse_args()


if args.trg_set_filename is not None:
  trg_set_filename = args.trg_set_filename
else:
  trg_set_filename = os.path.join('data', 'train')


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
  file_in = os.path.join('data', 'dev.in')


if args.file_out_p1 is not None:
  file_out_p1 = args.file_out_p1
else:
  file_out_p1 = 'dev.p1.out'


if args.file_out_p2 is not None:
  file_out_p2 = args.file_out_p2
else:
  file_out_p2 = 'dev.p2.out'


if args.file_gold is not None:
  file_gold = args.file_gold
else:
  file_gold = os.path.join('data', 'dev.out')





raw_data_filename = trg_set_filename
count_data_filename = count_data_filename
model_params_filename = model_params_filename

sys.stdout.write("Specified Traing Data File: %s\n" % raw_data_filename)
sys.stdout.write("Specified Count Data File: %s\n" % count_data_filename)
sys.stdout.write("Specified Model Params File: %s\n" % model_params_filename)

training_parser = TrgDataParser(raw_data_filename)
training_parser.read_raw_data()
training_parser.save_count_data(count_data_filename)
training_parser.generate_model_params()
training_parser.save_model_params(model_params_filename)


train_e_params=training_parser.e_params
train_q_params=training_parser.q_params
train_e_counts=training_parser.e_data_counter
train_q_counts=training_parser.q_data_counter
train_tag_counts=training_parser.tag_counter
y_list=[]
for i in train_tag_counts:
    y_list.append(i)

file_in=file_in
file_out_p1=file_out_p1
file_gold=file_gold
validate_tagger=SimpleTagger(train_e_params, train_e_counts, train_tag_counts,file_in,file_out_p1,file_gold)
validate_tagger.update_emission_parameters()
validate_tagger.run_simple_tagger()
validate_tagger.check_accuracy()
train_e_params=validate_tagger.emission_params


file_out_p2=file_out_p2
final_viterbi=ViterbiOptimizer(train_q_params,train_e_params,file_in,file_out_p2,file_gold,y_list)
final_viterbi.tokenize_input()
final_viterbi.tokenize_gold()
final_viterbi.run()
#print final_viterbi.start_params
final_viterbi.compare_accuracy()

compare_tweet_files(file_out_p2, file_gold)

sys.stdout.write("\n\n----- Completed Parse -----\n\n")
