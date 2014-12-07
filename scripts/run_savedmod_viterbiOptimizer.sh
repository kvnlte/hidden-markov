#!/bin/bash

python run_viterbiOptimizer_from_model_params_file.py -m model_params.csv -d dev.in -o dev.vitOptmod.out

python compare_tagged_output.py -i dev.vitOptmod.out -r dev.out

