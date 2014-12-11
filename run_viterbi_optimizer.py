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
from pre_process.pre_process_data import pre_process_data as prePD
from pre_process.post_process_data import post_process_data as postPD

sys.stdout.write("\n\n----- Beginning Parse -----\n\n")

parser = argparse.ArgumentParser()

parser.add_argument("-i", dest='trg_set_filename', type=str, help="training data file")
parser.add_argument("-o", dest='count_data_filename', type=str, help="count data file")
parser.add_argument("-p", dest='model_params_filename', type=str, help="model params data file")
parser.add_argument("-ti", dest='file_in', type=str, help="test data file without tags")
parser.add_argument("-to", dest='file_out', type=str, help="test data file with tags, phase 3")
parser.add_argument("-g", dest='file_gold', type=str, help="test data file with gold standard tags")
parser.add_argument("-c", dest='compare', help="Flag to decide whether or not to compare", action="store_true")
parser.add_argument("-p2", dest='p2', help="To indicate running of part 2", action="store_true")
parser.add_argument("-p3", dest='p3', help="To indicate running of part 3", action="store_true")


args = parser.parse_args()

if args.p2 and args.p3:
    raise RuntimeError("Ambiguous parts specified")
elif not args.p2 and not args.p3:
    raise RuntimeError("Part not specified")



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


if args.file_out is not None:
  file_out = args.file_out
elif args.p2:
  file_out = os.path.join('data','dev.p2.out')
elif args.p3:
    file_out = os.path.join('data','dev.p3.out')


if args.file_gold is not None:
  file_gold = args.file_gold
else:
  file_gold = os.path.join('data', 'dev.out')





raw_data_filename = trg_set_filename
count_data_filename = count_data_filename
model_params_filename = model_params_filename

sys.stdout.write("Specified Training Data File: %s\n" % raw_data_filename)
sys.stdout.write("Specified Test Data File: %s\n" % file_in)
sys.stdout.write("Specified Test Data Output Location: %s\n" % file_out)
if args.compare:
    sys.stdout.write("Specified Gold Test Data File: %s\n" % file_gold)


sys.stdout.write("Specified Count Data File: %s\n" % count_data_filename)
sys.stdout.write("Specified Model Params File: %s\n" % model_params_filename)



#print raw_data_filename
pptrain=trg_set_filename+'.pp'
#print pptrain
prePD(trg_set_filename,pptrain,'train')

ppfile_in=file_in+'.pp'
prePD(file_in,ppfile_in,'test')


if args.p2:
    pptrain=trg_set_filename
    ppfile_in=file_in
    bypassOpt=False
else:
    bypassOpt = True




model = ModelCalculator(pptrain)
model.load_test_file(ppfile_in)
model.init_model_params(bypassOpt)


train_q_params = model.q_params
train_e_params = model.e_params
#file_in = testdata_filename
#file_out = output_filename
#file_gold = os.path.join('data', 'dev.out')
states = model.tags_seen + ['*', 'STOP']

output_interm=file_out+'.int'

final_viterbi=ViterbiOptimizer(train_q_params,train_e_params,ppfile_in,output_interm,file_gold,states)
final_viterbi.tokenize_input()
final_viterbi.tokenize_gold()
final_viterbi.run()
#print final_viterbi.start_params




postPD(file_in,output_interm,file_out)


os.remove(output_interm)
if args.p3:
    os.remove(ppfile_in)
    os.remove(pptrain)

if args.compare:
    compare_tweet_files(file_out, file_gold)

sys.stdout.write("\n\n----- Completed Parse -----\n\n")
