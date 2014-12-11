import sys
from collections import Counter
import argparse
import csv

from raw_parser import TrgDataParser
from simple_pos_tagger import SimpleTagger
from viterbi_optimizer_phase3 import ViterbiOptimizerP3



#raw_data_filename = 'train'
#count_data_filename = 'train_data_count.csv'
#model_params_filename = 'train_model_params.csv'
#sys.stdout.write("Specified Traing Data File: %s\n" % raw_data_filename)
#sys.stdout.write("Specified Count Data File: %s\n" % count_data_filename)
#sys.stdout.write("Specified Model Params File: %s\n" % model_params_filename)
#
#training_parser = TrgDataParser(raw_data_filename)
#training_parser.read_raw_data()
#training_parser.save_count_data(count_data_filename)
#training_parser.generate_model_params()
#training_parser.save_model_params(model_params_filename)
#
#
#train_e_params=training_parser.get_e_params()
#train_q_params=training_parser.get_q_params()
#train_e_counts=training_parser.get_e_data_counter()
#train_q_counts=training_parser.get_q_data_counter()
#train_tag_counts=training_parser.get_tag_counter()
#y_list=[]
#for i in train_tag_counts:
#    y_list.append(i)
#
#file_in='dev.in'
#file_out='dev.p1.out'
#file_gold='dev.out'
#validate_tagger=SimpleTagger(train_e_params, train_e_counts, train_tag_counts,file_in,file_out,file_gold)
#validate_tagger.update_emission_parameters()
#validate_tagger.run_simple_tagger()
#validate_tagger.check_accuracy()
#train_e_params=validate_tagger.emission_params
#
#
#file_out='dev.p2.out'
#final_viterbi=ViterbiOptimizer(train_q_params,train_e_params,file_in,file_out,file_gold,y_list)
#final_viterbi.tokenize_input()
#final_viterbi.tokenize_gold()
#final_viterbi.run()
##print final_viterbi.start_params
#final_viterbi.compare_accuracy()


###############################################################################

if __name__ == "__main__":
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

    raw_data_filename = args.trg_set_filename
    count_data_filename = args.count_data_filename
    model_params_filename = args.model_params_filename

    sys.stdout.write("Specified Traing Data File: %s\n" % raw_data_filename)
    sys.stdout.write("Specified Count Data File: %s\n" % count_data_filename)
    sys.stdout.write("Specified Model Params File: %s\n" % model_params_filename)

    training_parser = TrgDataParser(raw_data_filename)
    training_parser.read_raw_data()
    training_parser.save_count_data(count_data_filename)
    training_parser.generate_model_params()
    training_parser.save_model_params(model_params_filename)


    train_e_params=training_parser.get_e_params()
    train_q_params=training_parser.get_q_params()
    train_e_counts=training_parser.get_e_data_counter()
    train_q_counts=training_parser.get_q_data_counter()
    train_tag_counts=training_parser.get_tag_counter()
    y_list=[]
    for i in train_tag_counts:
        y_list.append(i)
    
    file_in=args.file_in
    file_out_p1=args.file_out_p1
    file_gold=args.file_gold
    validate_tagger=SimpleTagger(train_e_params, train_e_counts, train_tag_counts,file_in,file_out_p1,file_gold)
    validate_tagger.update_emission_parameters()
    validate_tagger.run_simple_tagger()
    validate_tagger.check_accuracy()
    train_e_params=validate_tagger.emission_params
    
    
    file_out_p2=args.file_out_p2
    final_viterbi=ViterbiOptimizerP3(train_q_params,train_e_params,file_in,file_out_p2,file_gold,y_list)
    final_viterbi.tokenize_input()
    final_viterbi.tokenize_gold()
    final_viterbi.run()
    #print final_viterbi.start_params
    final_viterbi.compare_accuracy()
    

    sys.stdout.write("\n\n----- Completed Parse -----\n\n")
