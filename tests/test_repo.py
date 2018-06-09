#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier:     MIT

"""
    Unit tests for pointilist.repo.
"""

import unittest

import os
import sys
from io import StringIO

from pointilist import repo


class TestConstructor(unittest.TestCase):
    """Tests the Repo() constructor."""

    def setUp(self):
        self.dir = None
        if 'POINTILIST_TEST_BASEDIR' in os.environ:
            self.dir = os.environ['POINTILIST_TEST_BASEDIR']

    def test_repo(self):
        """Check if the working directory is correctly created and deleted."""

        with repo.Repo(tempdir=self.dir) as r:
            self.assertTrue(os.path.isdir(r.tempdir))

        self.assertFalse(os.path.exists(r.tempdir))


class TestPopulateMethod(unittest.TestCase):
    """Tests for the Repo.populate() method."""

    def setUp(self):
        self.dir = None
        if 'POINTILIST_TEST_BASEDIR' in os.environ:
            self.dir = os.environ['POINTILIST_TEST_BASEDIR']

    def test_populate_empty_data(self):
        """Check ."""

        sys.stderr = StringIO()

        with repo.Repo(tempdir=self.dir) as r:
            r.populate([])

        self.assertNotEqual(
            -1,
            sys.stderr.getvalue().strip().find('Commit data missing')
        )

        sys.stderr = sys.__stderr__
