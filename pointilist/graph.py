#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier:     MIT

"""
    Handles the interaction with github contribution graph data.

    :copyright: © 2018, tickelton <tickelton@gmail.com>.
    :license: MIT, see LICENSE for details.
"""

import urllib.request


class Graph:
    """Object that represents a user's github contribution graph."""

    def __init__(self, username):
        self.username = username

    def fetch(self):
        """Retrieves contribution data from Github."""

        url = 'https://github.com/users/' + self.username + '/contributions'
        page = urllib.request.urlopen(url)

        return page.readlines()
