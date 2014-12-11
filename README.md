hidden-markov
=============

The model parameters as trained by the program will be stored in model_params.csv, in the following format:

type | first_term | second_term | value
---- | ---------- | ----------- | -----
e    | x          | y           | e( x given y )
q    | y(i)       | y(i-1)      | q( y(i) given y(i-1) )


The training data will also be evaluated, and stored in eval_trgdata.csv in the following format:

type    | first_term | second_term | value
------- | ---------- | ----------- | -----
e       | x          | y           | count( y -> x )
q       | y(i)       | y(i-1)      | count( y(i-1) -> y(i) )
(none)  | y          | (none)      | count( y )


To run challenge:
python run_viterbi_optimizer.py -i data/combined_train -ti data/test.in -to test.p3.out
