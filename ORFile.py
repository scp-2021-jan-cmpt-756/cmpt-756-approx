#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
  Read in a file from the set cover portion of Beasley's OR data set library
  See http://people.brunel.ac.uk/~mastjjb/jeb/orlib/scpinfo.html
  This code extends Beaseley's orginal file format to include
  comment lines, indicated by a leading '#', possibly preceded by whitespace.

  Pseudo-comments begin with '##'
  1. The pseudo-comment '##setfile' indicates that the set list
     is not in Beasley's OR format but instead is simply a list of
     sets, with each set represented by a list of the items it contains.
     This pseudo-comment can be placed at any point in the file. Conventionally
     it is placed just before the list of sets.

  The class reads the entire file into memory and retains that memory as
  long as the object instance exists.

  Ill-formatted files produce assertion errors.

"""

from functools import reduce

# Just for testing
from sys import argv

class SetCover():
    '''
      Represent a set covering instance.
      The universe of elements is a dense sequence of non-negative values
      starting at 0.
    '''
    def __init__(self, universe_count, list_of_sets, weights):
        '''
          list_of_sets may contain repeat values.  The weights list
          will have an entry for each instance.  The last weight
          associated with these instances will be chosen as the unique weight.
          This odd design is required because the OR Library files have
          multiple repeated values.
        '''
        assert 0 < universe_count
        assert type(list_of_sets) == list
        assert len(weights) == len(list_of_sets)
        flatten = set()
        for s in list_of_sets:
            flatten |= s
        assert (0 == min(flatten) and
                max(flatten) == universe_count-1 and
                len(flatten) == universe_count)
        assert 0 < min(weights)

        list_of_sets = [frozenset(l) for l in list_of_sets]
        self.sets = set(list_of_sets)
        self.weight_list = weights
        self.weight_lookup = {}
        for i, s in enumerate(list_of_sets):
            self.weight_lookup[s] = self.weight_list[i]
        self._inf_weight = max(self.weight_list) + 1
        self.universe_count = universe_count

    def set_of_sets(self):
        ''' Return the set-of-frozensets that will form the cover '''
        return self.sets

    def universe(self):
        ''' Return the universe for this set cover instance '''
        return set(range(self.universe_count))

    def weight(self, a_set):
        ''' Return the weight for a_set '''
        return self.weight_lookup[a_set]

    def inf_weight(self):
        ''' Return a weight greater than any set's weight '''
        return self._inf_weight

    def check_solution(self, sol):
        ''' Check that a proposed solution covers the set '''
        # Check that solution is from the list of sets
        if any(s not in self.sets for s in sol):
            return False
        # Check that solution covers universe
        return reduce(lambda a, b: a|b, sol, set()) == self.universe()

class IntStream():
    '''
      Read a file that is a stream of integers, possibly with comment
      lines indicated by a leading '#'.
    '''
    def __init__(self, fname):
        ''' Read the file entirely into memory '''
        self.type = 'orfile' # default
        self.ints = []
        with open(fname, 'r', encoding='utf-8') as inp:
            line = inp.readline().strip()
            while line != '':
                if line[0] != '#':
                    self.ints.extend([int(s) for s in line.split()])
                elif line[1:] == '#setfile':
                    self.type='setfile'
                line = inp.readline().strip()
        self.next = 0

    def get_int(self):
        ''' Get the next integer from the stream '''
        assert self.next < len(self.ints)
        self.next += 1
        return self.ints[self.next-1]

    def get_seq(self, count):
        ''' Get the next count integers from the stream '''
        assert self.next + count <= len(self.ints)
        self.next += count
        return self.ints[self.next-count:self.next]

    def assert_empty(self):
        '''
            Assert that the stream is now empty.
            Call this to check that there are no trailing values.
        '''
        assert self.next == len(self.ints)

class ORFile():
    '''
      Read and write files formatted according to OR Library conventions. See
      file header comment for URL describing file format.
    '''
    def __init__(self, fname):
        ''' Read in a set cover problem instance '''
        stream = IntStream(fname)
        if stream.type == 'setfile':
            self.set_cover = SetFile(fname).get_set_cover()
            return
        universe_count = stream.get_int()
        set_count = stream.get_int()
        weight_list = stream.get_seq(set_count)
        element_member = []
        for i in range(set_count):
            element_member.append([])
        for i in range(universe_count):
            count = stream.get_int()
            for s in stream.get_seq(count):
                assert 1 <= s <= len(element_member)
                element_member[s-1].append(i)
        stream.assert_empty()
        element_member = [frozenset(l) for l in element_member]
        self.set_cover = SetCover(universe_count, element_member, weight_list)

    def get_set_cover(self):
        ''' Return the set cover instance that was read in '''
        return self.set_cover

    @staticmethod
    def write_set_cover(sc, fname):
        ''' Write a set cover instance to file fname '''
        # Invert the table
        items = []
        for i in range(len(sc.universe())):
            items.append([])
        for ind, s in enumerate(sc.set_of_sets()):
            print(ind, s)
            for v in s:
                items[v].append(ind)

        with open(fname, 'w', encoding='UTF-8') as out:
            out.write('# Universe count\n{}\n'.format(len(sc.universe())))
            out.write('# Number of sets\n{}\n'.format(len(sc.set_of_sets())))
            out.write('# Weights\n')
            for s in sc.set_of_sets():
                out.write('{} '.format(sc.weight(s)))
            out.write('\n')
            for i, ss in enumerate(items):
                out.write('# Item {}\n'.format(i))
                out.write('{}\n'.format(len(ss)))
                for v in ss:
                    out.write('{} '.format(v+1))
                out.write('\n')

class SetFile():
    '''
      Read and write files formatted according to set-oriented conventions.
      This format is the same for universe, set count, and weights but
      represents the sets explicitly.  Each set is represented by a count,
      followed by a list of that many values, which are the
      values it contains.

      Note that the Beasley format represents values using 1-origin
      indexing while this format uses 0-origin indexing.

      This format does not accept replicated sets.
    '''
    def __init__(self, fname):
        ''' Read in a set cover problem instance '''
        stream = IntStream(fname)
        assert stream.type == 'setfile'
        universe_count = stream.get_int()
        set_count = stream.get_int()
        weight_list = stream.get_seq(set_count)
        element_member = []
        for i in range(set_count):
            count = stream.get_int()
            s = frozenset(stream.get_seq(count))
            assert all(v in range(universe_count) for v in s)
            assert s not in element_member
            element_member.append(s)
        stream.assert_empty()
        self.set_cover = SetCover(universe_count, element_member, weight_list)

    def get_set_cover(self):
        ''' Return the set cover instance that was read in '''
        return self.set_cover

if __name__ == '__main__':
    ''' Run single test '''
    instance = ORFile(argv[1]).get_set_cover()
    print(len(instance.sets))
