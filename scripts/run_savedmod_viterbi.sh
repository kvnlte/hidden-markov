#!/bin/bash

python run_viterbi_from_model_params_file.py -m model_params.csv -d dev.in -o dev.vitmod.out

python compare_tagged_output.py -i dev.vitmod.out -r dev.out

