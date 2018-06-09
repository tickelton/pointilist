#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier:     MIT

"""
    Handles the interaction with the git repository.

    :copyright: © 2018, tickelton <tickelton@gmail.com>.
    :license: MIT, see LICENSE for details.
"""

import logging
import shutil
import tempfile


class Repo:
    """Object that represents an actual git repository."""

    def __init__(self, commits, tempdir=None):
        self.commits = commits
        self.tempdir = tempfile.mkdtemp(dir=tempdir)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        shutil.rmtree(self.tempdir)

    def populate(self):
        """Populates the repository with fake commits."""

        if not self.commits:
            logging.warning('Commit data missing.')
            return

        if not [True for c in self.commits if c['count'] > 0]:
            logging.warning('Nothing to commit.')
            return
