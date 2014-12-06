#!/bin/bash

echo
echo "WARNING: this will overwrite the current model_params.csv, if it exits"
echo

python viterbi_algo.py -t train -d dev.in -o dev.vit2.out -m model_params.csv

python compare_tagged_output.py -i dev.vit2.out -r dev.out
