#! /usr/bin/env python

import unittest
from unittest import mock
from mock import patch
from parameterized import parameterized, parameterized_class

import sys
import logging
import numpy as np
from Bio import AlignIO
import os
from os import path

import CIAlign

import CIAlign.parsingFunctions as parsingFunctions

class cleaningFunctionsTests(unittest.TestCase):

    def setUp(self):

        self.in_array = []
        self.nams = []
        input_ali = AlignIO.read(open("./tests/test_files/example1.fasta"), "fasta")
        for record in input_ali:
            self.in_array.append(record.seq)
            self.nams.append(record.id)
        self.in_array = np.array(self.in_array)
        self.relativePositions = list(range(0, len(self.in_array[0])))
        self.rm_file = 'mock_rmfile.txt'


    def tearDown(self):
        os.remove(self.rm_file)

    @parameterized.expand([
            [0.05, 0.1, "./tests/test_files/crop_ends_cleaned.fasta", ],
            [0.6, 0.1, "./tests/test_files/example1.fasta", ],
            [0.05, 0.05, "./tests/test_files/example1.fasta", ],
    ])
    def test_cropEnds(self, mingap, redefine_perc, expected):

        exp_array = []
        expected_ali = AlignIO.read(open(expected), "fasta")
        exp_array = np.array([list(rec) for rec in expected_ali])
        exp_array = np.array(exp_array)

        logger = logging.getLogger('path.to.module.under.test')
        with mock.patch.object(logger, 'debug') as mock_debug:
            result_ali, names = parsingFunctions.cropEnds(self.in_array, self.nams, self.relativePositions, self.rm_file, mock_debug, mingap, redefine_perc)

        self.assertEqual(result_ali[0,:].size, exp_array[0,:].size)
        self.assertEqual(len(self.in_array), len(result_ali))
        self.assertTrue((result_ali == exp_array).all())

    @parameterized.expand([
            [3, 100, 5, "./tests/test_files/remove_insertions_cleaned.fasta", ],
            [20, 100, 5, "./tests/test_files/example1.fasta", ],
            [3, 100, 30, "./tests/test_files/example1.fasta", ],
    ])
    def test_removeInsertions(self, min_size, max_size, min_flank, expected):

        exp_array = []
        expected_ali = AlignIO.read(open(expected), "fasta")
        exp_array = np.array([list(rec) for rec in expected_ali])
        exp_array = np.array(exp_array)

        logger = logging.getLogger('path.to.module.under.test')
        with mock.patch.object(logger, 'debug') as mock_debug:
            result_ali, r, self.relativePositions = parsingFunctions.removeInsertions(self.in_array, self.relativePositions, self.rm_file, mock_debug, min_size, max_size, min_flank)
        # check if dimensions are equal first
        self.assertEqual(result_ali[0,:].size, exp_array[0,:].size)
        self.assertEqual(len(self.in_array), len(result_ali))
        self.assertTrue((result_ali == exp_array).all())

    @parameterized.expand([
            [0.75, "./tests/test_files/remove_divergent_cleaned.fasta", ],
            [0.1,  "./tests/test_files/example1.fasta", ],
    ])
    def test_removeDivergent(self, percidentity, expected):

        exp_array = []
        expected_ali = AlignIO.read(open(expected), "fasta")
        exp_array = np.array([list(rec) for rec in expected_ali])
        exp_array = np.array(exp_array)

        logger = logging.getLogger('path.to.module.under.test')
        with mock.patch.object(logger, 'debug') as mock_debug:
            result_ali, r = parsingFunctions.removeDivergent(self.in_array, self.nams, self.rm_file, mock_debug, percidentity)

        self.assertEqual(result_ali[0,:].size, exp_array[0,:].size)
        self.assertEqual(result_ali[:,0].size, exp_array[:,0].size)
        self.assertGreaterEqual(len(self.in_array), len(result_ali))
        self.assertTrue((result_ali == exp_array).all())

    @parameterized.expand([
            [50, "./tests/test_files/remove_short_cleaned.fasta", ],
            [10,  "./tests/test_files/example1.fasta", ],
    ])
    def test_removeShort(self, min_length, expected):

        exp_array = []
        expected_ali = AlignIO.read(open(expected), "fasta")
        exp_array = np.array([list(rec) for rec in expected_ali])
        exp_array = np.array(exp_array)

        logger = logging.getLogger('path.to.module.under.test')
        with mock.patch.object(logger, 'debug') as mock_debug:
            result_ali, r = parsingFunctions.removeTooShort(self.in_array, self.nams, self.rm_file, mock_debug, min_length)

        self.assertTrue((result_ali == exp_array).all())
        self.assertGreaterEqual(len(self.in_array), len(result_ali))

    def test_removeGapOnly(self):

        expected = "./tests/test_files/remove_gaponly_cleaned.fasta"
        exp_array = []
        expected_ali = AlignIO.read(open(expected), "fasta")
        exp_array = np.array([list(rec) for rec in expected_ali])
        exp_array = np.array(exp_array)

        logger = logging.getLogger('path.to.module.under.test')
        with mock.patch.object(logger, 'debug') as mock_debug:
            result_ali, r, self.relativePositions = parsingFunctions.removeGapOnly(self.in_array, self.relativePositions, self.rm_file, mock_debug)

        self.assertTrue((result_ali == exp_array).all())
        self.assertEqual(len(self.in_array), len(result_ali))

if __name__ == '__main__':
    unittest.main(warnings='ignore')
