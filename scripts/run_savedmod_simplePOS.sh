#!/bin/bash

python run_simplePOS_tagger_without_param_modification.py -m model_params.csv -d dev.in -o dev.p2.out

python compare_tagged_output.py -i dev.p2.out -r dev.out
