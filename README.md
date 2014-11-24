hidden-markov
=============

The model parameters as trained by the program will be stored in model_params.csv, in the following format:

type | first_term | second_term | value
---- | ---------- | ----------- | -----
e    | x          | y           | e( y -> x )
q    | y(i)       | y(i-1)      | q( y(i-1) -> y(y(i) )


The training data will also be evaluated, and stored in eval_trgdata.csv in the following format:

type    | first_term | second_term | value
------- | ---------- | ----------- | -----
e       | x          | y           | count( y -> x )
q       | y(i)       | y(i-1)      | count( y(i-1) -> y(i) )
<empty> | x          | <empty>           | count( x )

