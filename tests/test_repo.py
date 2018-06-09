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

COMMITS_ZERO_COUNT = [
    {
        'date': '2018-05-04',
        'count': 0
    },
    {
        'date': '2018-05-05',
        'count': 0
    }
]
COMMITS_VALID = [
    {
        'date': '2018-05-04',
        'count': 0
    },
    {
        'date': '2018-05-05',
        'count': 3
    }
]

FAKE_STDERR = StringIO()


class TestConstructor(unittest.TestCase):
    """Tests the Repo() constructor."""

    def setUp(self):
        self.dir = None
        if 'POINTILIST_TEST_BASEDIR' in os.environ:
            self.dir = os.environ['POINTILIST_TEST_BASEDIR']

    def test_repo_missing_commits_argument(self):
        """Check behaviour on missing argument."""

        with self.assertRaises(TypeError):
            with repo.Repo():
                pass

    def test_repo_valid(self):
        """Check if the working directory is correctly created and deleted."""

        with repo.Repo([], tempdir=self.dir) as r:
            self.assertTrue(os.path.isdir(r.tempdir))

        self.assertFalse(os.path.exists(r.tempdir))


class TestPopulateMethod(unittest.TestCase):
    """Tests for the Repo.populate() method."""

    def setUp(self):
        sys.stderr = FAKE_STDERR
        self.dir = None
        if 'POINTILIST_TEST_BASEDIR' in os.environ:
            self.dir = os.environ['POINTILIST_TEST_BASEDIR']

    def tearDown(self):
        sys.stderr = sys.__stderr__

    def test_populate_empty_data(self):
        """Check behaviour for empty commit list."""

        with repo.Repo([], tempdir=self.dir) as r:
            r.populate()

        self.assertNotEqual(
            -1,
            sys.stderr.getvalue().strip().find('Commit data missing')
        )

    def test_populate_no_commits_to_create(self):
        """Check behaviour for datasets that do not result in commits."""

        with repo.Repo(COMMITS_ZERO_COUNT, tempdir=self.dir) as r:
            r.populate()

        self.assertNotEqual(
            -1,
            sys.stderr.getvalue().strip().find('Nothing to commit.')
        )
