#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier:     MIT

"""
    Handles the interaction with github contribution graph data.

    :copyright: © 2018, tickelton <tickelton@gmail.com>.
    :license: MIT, see LICENSE for details.
"""

import urllib.request
from urllib.error import URLError, HTTPError


class Graph:
    """Object that represents a user's github contribution graph."""

    def __init__(self, username):
        self.username = username

    def fetch(self):
        """Retrieves contribution data from Github."""
        url = 'https://github.com/users/' + self.username + '/contributions'
        try:
            page = urllib.request.urlopen(url)
        except HTTPError as err:
            print("There was a problem fetching data from {}".format(url))
            print('Error code: ', err.code)
            return None
        except URLError as err:
            print("There was a problem fetching data from {}".format(url))
            print('Reason: ', err.reason)
            return None

        return page.readlines()
