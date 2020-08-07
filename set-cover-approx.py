#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
   Framework for writing a set cover approximation algorithm.
'''
# Standard modules
import argparse
import time

# Local module for reading data files in Beasley Operations Research (OR)
# format
import ORFile

def parse_args():
    argp = argparse.ArgumentParser(description='Compute set cover, '
        'using either student-written greedy algorithm '
        'or slower naive optimal algorithm')
    argp.add_argument('input',
        help='Input file, in format of Beasley OR library or SetFile'
        )
    argp.add_argument('--check',
        action='store_true',
        help='Check that the result is correct'
        )
    argp.add_argument('--skip_print',
        action='store_true',
        help='Do not print the result'
        )
    argp.add_argument('--use_optimal',
        action='store_true',
        help='Call the MUCH SLOWER optimal algorithm instead of set_cover()'
        )
    return argp.parse_args()

# This is the ONLY FUNCTION that you should modify
def set_cover(universe, subsets):
    """
        Find a family of subsets that covers the universal set.
        universe: range(N), where N is the size of the universe
        subsets: set of frozensets, each a subset of the universe
        Return a subset of subsets that covers the universe.
        The result can be either:
        (i) a list of sets, or
        (ii) a set of frozensets (Python does not permit sets of sets).
    """
    # YOUR CODE GOES HERE
    return cover

'''
    Algorithm for computing optimal answer.
    Expressed recursively
    Not written to make most efficient use of Python!
    The greedy algorithm is faster and much simpler
'''
def get_subsols(s, setlist, uncovered):
    ''' Return all subsolutions that include set s '''
    sols = set()
    subsols = sub_cover(uncovered, setlist - {s})
    for subs in subsols:
        sols.add(subs | {s})
    return sols

def sub_cover(uncovered, setlist):
    '''
        Return all possible solutions of this subproblem.
        Result is a set of frozensets of frozensets
    '''
    sols = set()
    if len(setlist) == 0:
        return sols
    s = next(iter(setlist))
    new_uncovered = uncovered - s
    if new_uncovered == set():
      sols.add(frozenset([frozenset(s)]))
    else:
        sols |= get_subsols(s, setlist, new_uncovered)
    sols |= sub_cover(uncovered, setlist - {s})
    return sols

def optimum_set_cover(universe, setlist):
    ''' Top level call to recursive algorithm '''
    solutions = sub_cover(universe, setlist)
    # Return the smallest solution
    return min(solutions, key=lambda s: len(s))

def main(instance, args):
    ''' Run the selected algorithm and print the results '''
    if args.use_optimal:
        start = time.monotonic()
        cover = optimum_set_cover(instance.universe(), instance.set_of_sets())
        end = time.monotonic()
    else:
        start = time.monotonic()
        cover = set_cover(instance.universe(), instance.set_of_sets())
        end = time.monotonic()
    if args.check and not instance.check_solution(cover):
        print('*** Not a solution! ***')
    print(end-start)
    print(len(cover))
    if args.skip_print:
        return
    for s in cover:
        for v in s:
            print(v, end=' ')
        print()

if __name__ == '__main__':
    args = parse_args()
    instance = ORFile.ORFile(args.input).get_set_cover()
    main(instance, args)
