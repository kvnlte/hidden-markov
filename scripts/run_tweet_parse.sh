#!/bin/bash

# This script is intended to be run from the parent directory of its containing directory
# i.e. $ ./scripts/run_tweet_parse.sh

# The parent directory should contain the files 'parser.py' and 'train'
# Output from parser.py will be stored in the file 'eval_trgdata.csv' in the parent directory

python raw_parser.py -i train -o eval_trgdata.csv -p model_params.csv
python simple_pos_tagger.py -m model_params.csv -e eval_trgdata.csv -i dev.in -o mydev.out -g dev.out