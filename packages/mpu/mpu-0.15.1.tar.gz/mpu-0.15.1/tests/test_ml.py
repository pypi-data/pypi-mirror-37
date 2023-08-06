#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

# core modules
import unittest

# internal modules
import mpu.ml


class MLTest(unittest.TestCase):

    def test_negative_class_number(self):
        with self.assertRaises(ValueError):
            mpu.ml.indices2one_hot([0, 1, 1], 0)

    def test_indices2one_hot(self):
        """Doctest."""
        result = mpu.ml.indices2one_hot([0, 1, 1], 3)
        assert result == [[1, 0, 0], [0, 1, 0], [0, 1, 0]]
        result = mpu.ml.indices2one_hot([0, 1, 1], 2)
        assert result == [[1, 0], [0, 1], [0, 1]]
