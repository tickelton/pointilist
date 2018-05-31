#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# SPDX-License-Identifier:     MIT

import urllib3

class Graph:
    """Object that represents a user's github contribution graph."""

    def __init__(self, username):
        self.username = username

    def fetch(self):
        pass

