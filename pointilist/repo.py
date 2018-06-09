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

    def __init__(self, tempdir=None):
        self.tempdir = tempfile.mkdtemp(dir=tempdir)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        shutil.rmtree(self.tempdir)

    def populate(self, commits):
        """Populates the repository with fake commits."""

        if not commits:
            logging.warning('Commit data missing; len(commits) == 0')
            return

        #if not all([True for c in commits if c['count'] > 0]):
        #    logging.warning('Nothing to commit.')
        #    return
