This repository contains the template code and data for Assignment 1
in CMPT 756.

The file `set-cover-approx.py` is the skeleton code. You will modify
this file to add your version of greedy set cover. The main routine
will list its calling requirements and possible options when called
with the `-h` option:

~~~
$ ./set-cover-approx.py -h
usage: set-cover-approx.py [-h] [--check] [--skip_print] [--use_optimal] input
...
~~~

The file `ORFile.py` is a module called by `set-cover-approx.py` to
read the datasets and check the correctness of proposed results.  You
will not need to modify it, though you are welcome to look at the
code.

The files named `*.txt` are various datasets, which you can use to
test your code. You will use `worst-*.txt` in the third section of the
assignment. The files named `test-N.txt` are small files specifically
for testing your algorithm. Their solutions are of size `N`.

The file `table.csv` contains the results for the runs of the optimal
algorithm. You may use this file when writing up your analysis.

