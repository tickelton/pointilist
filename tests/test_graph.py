#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier:     MIT

"""
    Unit tests for pointilist.graph.
"""

import os
import unittest
import urllib.request
from urllib.error import HTTPError
from io import StringIO

from pointilist import graph

STATIC_DIR = os.path.dirname(os.path.realpath(__file__)) \
        + '/static/'
CONTRIB_HTML = STATIC_DIR + 'contributions.html'
GARBAGE_HTML = STATIC_DIR + 'hello_world.html'
SHORT_HTML = STATIC_DIR + 'contributions_short.html'
CLASS_HTML = STATIC_DIR + 'contributions_wrong_class.html'


VALID_GRAPH_REFERENCE_DATA = {
    'wdays': [
        {'x': -14, 'wday': 'Sun', 'display': False, 'y': 8},
        {'x': -14, 'wday': 'Mon', 'display': True, 'y': 20},
        {'x': -14, 'wday': 'Tue', 'display': False, 'y': 32},
        {'x': -14, 'wday': 'Wed', 'display': True, 'y': 44},
        {'x': -14, 'wday': 'Thu', 'display': False, 'y': 57},
        {'x': -14, 'wday': 'Fri', 'display': True, 'y': 69},
        {'x': -14, 'wday': 'Sat', 'display': False, 'y': 81}
    ],
    'months': [
        {'x': 25, 'y': -10, 'month': 'Jun'},
        {'x': 73, 'y': -10, 'month': 'Jul'},
        {'x': 133, 'y': -10, 'month': 'Aug'},
        {'x': 181, 'y': -10, 'month': 'Sep'},
        {'x': 229, 'y': -10, 'month': 'Oct'},
        {'x': 289, 'y': -10, 'month': 'Nov'},
        {'x': 337, 'y': -10, 'month': 'Dec'},
        {'x': 397, 'y': -10, 'month': 'Jan'},
        {'x': 445, 'y': -10, 'month': 'Feb'},
        {'x': 493, 'y': -10, 'month': 'Mar'},
        {'x': 541, 'y': -10, 'month': 'Apr'},
        {'x': 601, 'y': -10, 'month': 'May'}
    ],
    'rects': [
        {'count': 3, 'date': '2017-05-28', 'x': 13, 'y': 0, 'fill': '#239a3b'},
        {'count': 3, 'date': '2017-05-29', 'x': 13, 'y': 12, 'fill': '#239a3b'},
        {'count': 3, 'date': '2017-05-30', 'x': 13, 'y': 24, 'fill': '#239a3b'},
        {'count': 0, 'date': '2017-05-31', 'x': 13, 'y': 36, 'fill': '#ebedf0'},
        {'count': 3, 'date': '2017-06-01', 'x': 13, 'y': 48, 'fill': '#239a3b'},
        {'count': 3, 'date': '2017-06-02', 'x': 13, 'y': 60, 'fill': '#239a3b'},
        {'count': 2, 'date': '2017-06-03', 'x': 13, 'y': 72, 'fill': '#7bc96f'},
        {'count': 1, 'date': '2017-06-04', 'x': 12, 'y': 0, 'fill': '#c6e48b'},
        {'count': 2, 'date': '2017-06-05', 'x': 12, 'y': 12, 'fill': '#7bc96f'},
        {'count': 2, 'date': '2017-06-06', 'x': 12, 'y': 24, 'fill': '#7bc96f'},
        {'count': 3, 'date': '2017-06-07', 'x': 12, 'y': 36, 'fill': '#239a3b'},
        {'count': 2, 'date': '2017-06-08', 'x': 12, 'y': 48, 'fill': '#7bc96f'},
        {'count': 0, 'date': '2017-06-09', 'x': 12, 'y': 60, 'fill': '#ebedf0'},
        {'count': 2, 'date': '2017-06-10', 'x': 12, 'y': 72, 'fill': '#7bc96f'},
        {'count': 2, 'date': '2017-06-11', 'x': 11, 'y': 0, 'fill': '#7bc96f'},
        {'count': 3, 'date': '2017-06-12', 'x': 11, 'y': 12, 'fill': '#239a3b'},
        {'count': 3, 'date': '2017-06-13', 'x': 11, 'y': 24, 'fill': '#239a3b'},
        {'count': 3, 'date': '2017-06-14', 'x': 11, 'y': 36, 'fill': '#239a3b'},
        {'count': 3, 'date': '2017-06-15', 'x': 11, 'y': 48, 'fill': '#239a3b'},
        {'count': 1, 'date': '2017-06-16', 'x': 11, 'y': 60, 'fill': '#c6e48b'},
        {'count': 0, 'date': '2017-06-17', 'x': 11, 'y': 72, 'fill': '#ebedf0'},
        {'count': 2, 'date': '2017-06-18', 'x': 10, 'y': 0, 'fill': '#7bc96f'},
        {'count': 3, 'date': '2017-06-19', 'x': 10, 'y': 12, 'fill': '#239a3b'},
        {'count': 0, 'date': '2017-06-20', 'x': 10, 'y': 24, 'fill': '#ebedf0'},
        {'count': 1, 'date': '2017-06-21', 'x': 10, 'y': 36, 'fill': '#c6e48b'},
        {'count': 1, 'date': '2017-06-22', 'x': 10, 'y': 48, 'fill': '#c6e48b'},
        {'count': 1, 'date': '2017-06-23', 'x': 10, 'y': 60, 'fill': '#c6e48b'},
        {'count': 1, 'date': '2017-06-24', 'x': 10, 'y': 72, 'fill': '#c6e48b'},
        {'count': 0, 'date': '2017-06-25', 'x': 9, 'y': 0, 'fill': '#ebedf0'},
        {'count': 2, 'date': '2017-06-26', 'x': 9, 'y': 12, 'fill': '#7bc96f'},
        {'count': 3, 'date': '2017-06-27', 'x': 9, 'y': 24, 'fill': '#239a3b'},
        {'count': 3, 'date': '2017-06-28', 'x': 9, 'y': 36, 'fill': '#239a3b'},
        {'count': 2, 'date': '2017-06-29', 'x': 9, 'y': 48, 'fill': '#7bc96f'},
        {'count': 1, 'date': '2017-06-30', 'x': 9, 'y': 60, 'fill': '#c6e48b'},
        {'count': 2, 'date': '2017-07-01', 'x': 9, 'y': 72, 'fill': '#7bc96f'},
        {'count': 0, 'date': '2017-07-02', 'x': 8, 'y': 0, 'fill': '#ebedf0'},
        {'count': 2, 'date': '2017-07-03', 'x': 8, 'y': 12, 'fill': '#7bc96f'},
        {'count': 1, 'date': '2017-07-04', 'x': 8, 'y': 24, 'fill': '#c6e48b'},
        {'count': 1, 'date': '2017-07-05', 'x': 8, 'y': 36, 'fill': '#c6e48b'},
        {'count': 2, 'date': '2017-07-06', 'x': 8, 'y': 48, 'fill': '#7bc96f'},
        {'count': 3, 'date': '2017-07-07', 'x': 8, 'y': 60, 'fill': '#239a3b'},
        {'count': 0, 'date': '2017-07-08', 'x': 8, 'y': 72, 'fill': '#ebedf0'},
        {'count': 2, 'date': '2017-07-09', 'x': 7, 'y': 0, 'fill': '#7bc96f'},
        {'count': 1, 'date': '2017-07-10', 'x': 7, 'y': 12, 'fill': '#c6e48b'},
        {'count': 3, 'date': '2017-07-11', 'x': 7, 'y': 24, 'fill': '#239a3b'},
        {'count': 0, 'date': '2017-07-12', 'x': 7, 'y': 36, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2017-07-13', 'x': 7, 'y': 48, 'fill': '#ebedf0'},
        {'count': 2, 'date': '2017-07-14', 'x': 7, 'y': 60, 'fill': '#7bc96f'},
        {'count': 2, 'date': '2017-07-15', 'x': 7, 'y': 72, 'fill': '#7bc96f'},
        {'count': 2, 'date': '2017-07-16', 'x': 6, 'y': 0, 'fill': '#7bc96f'},
        {'count': 2, 'date': '2017-07-17', 'x': 6, 'y': 12, 'fill': '#7bc96f'},
        {'count': 2, 'date': '2017-07-18', 'x': 6, 'y': 24, 'fill': '#7bc96f'},
        {'count': 3, 'date': '2017-07-19', 'x': 6, 'y': 36, 'fill': '#239a3b'},
        {'count': 3, 'date': '2017-07-20', 'x': 6, 'y': 48, 'fill': '#239a3b'},
        {'count': 2, 'date': '2017-07-21', 'x': 6, 'y': 60, 'fill': '#7bc96f'},
        {'count': 1, 'date': '2017-07-22', 'x': 6, 'y': 72, 'fill': '#c6e48b'},
        {'count': 3, 'date': '2017-07-23', 'x': 5, 'y': 0, 'fill': '#239a3b'},
        {'count': 1, 'date': '2017-07-24', 'x': 5, 'y': 12, 'fill': '#c6e48b'},
        {'count': 2, 'date': '2017-07-25', 'x': 5, 'y': 24, 'fill': '#7bc96f'},
        {'count': 0, 'date': '2017-07-26', 'x': 5, 'y': 36, 'fill': '#ebedf0'},
        {'count': 2, 'date': '2017-07-27', 'x': 5, 'y': 48, 'fill': '#7bc96f'},
        {'count': 1, 'date': '2017-07-28', 'x': 5, 'y': 60, 'fill': '#c6e48b'},
        {'count': 2, 'date': '2017-07-29', 'x': 5, 'y': 72, 'fill': '#7bc96f'},
        {'count': 0, 'date': '2017-07-30', 'x': 4, 'y': 0, 'fill': '#ebedf0'},
        {'count': 2, 'date': '2017-07-31', 'x': 4, 'y': 12, 'fill': '#7bc96f'},
        {'count': 1, 'date': '2017-08-01', 'x': 4, 'y': 24, 'fill': '#c6e48b'},
        {'count': 0, 'date': '2017-08-02', 'x': 4, 'y': 36, 'fill': '#ebedf0'},
        {'count': 2, 'date': '2017-08-03', 'x': 4, 'y': 48, 'fill': '#7bc96f'},
        {'count': 3, 'date': '2017-08-04', 'x': 4, 'y': 60, 'fill': '#239a3b'},
        {'count': 3, 'date': '2017-08-05', 'x': 4, 'y': 72, 'fill': '#239a3b'},
        {'count': 0, 'date': '2017-08-06', 'x': 3, 'y': 0, 'fill': '#ebedf0'},
        {'count': 1, 'date': '2017-08-07', 'x': 3, 'y': 12, 'fill': '#c6e48b'},
        {'count': 3, 'date': '2017-08-08', 'x': 3, 'y': 24, 'fill': '#239a3b'},
        {'count': 2, 'date': '2017-08-09', 'x': 3, 'y': 36, 'fill': '#7bc96f'},
        {'count': 2, 'date': '2017-08-10', 'x': 3, 'y': 48, 'fill': '#7bc96f'},
        {'count': 3, 'date': '2017-08-11', 'x': 3, 'y': 60, 'fill': '#239a3b'},
        {'count': 3, 'date': '2017-08-12', 'x': 3, 'y': 72, 'fill': '#239a3b'},
        {'count': 3, 'date': '2017-08-13', 'x': 2, 'y': 0, 'fill': '#239a3b'},
        {'count': 1, 'date': '2017-08-14', 'x': 2, 'y': 12, 'fill': '#c6e48b'},
        {'count': 0, 'date': '2017-08-15', 'x': 2, 'y': 24, 'fill': '#ebedf0'},
        {'count': 3, 'date': '2017-08-16', 'x': 2, 'y': 36, 'fill': '#239a3b'},
        {'count': 2, 'date': '2017-08-17', 'x': 2, 'y': 48, 'fill': '#7bc96f'},
        {'count': 0, 'date': '2017-08-18', 'x': 2, 'y': 60, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2017-08-19', 'x': 2, 'y': 72, 'fill': '#ebedf0'},
        {'count': 1, 'date': '2017-08-20', 'x': 1, 'y': 0, 'fill': '#c6e48b'},
        {'count': 0, 'date': '2017-08-21', 'x': 1, 'y': 12, 'fill': '#ebedf0'},
        {'count': 1, 'date': '2017-08-22', 'x': 1, 'y': 24, 'fill': '#c6e48b'},
        {'count': 3, 'date': '2017-08-23', 'x': 1, 'y': 36, 'fill': '#239a3b'},
        {'count': 1, 'date': '2017-08-24', 'x': 1, 'y': 48, 'fill': '#c6e48b'},
        {'count': 0, 'date': '2017-08-25', 'x': 1, 'y': 60, 'fill': '#ebedf0'},
        {'count': 2, 'date': '2017-08-26', 'x': 1, 'y': 72, 'fill': '#7bc96f'},
        {'count': 3, 'date': '2017-08-27', 'x': 0, 'y': 0, 'fill': '#239a3b'},
        {'count': 2, 'date': '2017-08-28', 'x': 0, 'y': 12, 'fill': '#7bc96f'},
        {'count': 2, 'date': '2017-08-29', 'x': 0, 'y': 24, 'fill': '#7bc96f'},
        {'count': 2, 'date': '2017-08-30', 'x': 0, 'y': 36, 'fill': '#7bc96f'},
        {'count': 2, 'date': '2017-08-31', 'x': 0, 'y': 48, 'fill': '#7bc96f'},
        {'count': 0, 'date': '2017-09-01', 'x': 0, 'y': 60, 'fill': '#ebedf0'},
        {'count': 2, 'date': '2017-09-02', 'x': 0, 'y': 72, 'fill': '#7bc96f'},
        {'count': 2, 'date': '2017-09-03', 'x': -1, 'y': 0, 'fill': '#7bc96f'},
        {'count': 2, 'date': '2017-09-04', 'x': -1, 'y': 12, 'fill': '#7bc96f'},
        {'count': 1, 'date': '2017-09-05', 'x': -1, 'y': 24, 'fill': '#c6e48b'},
        {'count': 3, 'date': '2017-09-06', 'x': -1, 'y': 36, 'fill': '#239a3b'},
        {'count': 1, 'date': '2017-09-07', 'x': -1, 'y': 48, 'fill': '#c6e48b'},
        {'count': 1, 'date': '2017-09-08', 'x': -1, 'y': 60, 'fill': '#c6e48b'},
        {'count': 2, 'date': '2017-09-09', 'x': -1, 'y': 72, 'fill': '#7bc96f'},
        {'count': 0, 'date': '2017-09-10', 'x': -2, 'y': 0, 'fill': '#ebedf0'},
        {'count': 1, 'date': '2017-09-11', 'x': -2, 'y': 12, 'fill': '#c6e48b'},
        {'count': 2, 'date': '2017-09-12', 'x': -2, 'y': 24, 'fill': '#7bc96f'},
        {'count': 0, 'date': '2017-09-13', 'x': -2, 'y': 36, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2017-09-14', 'x': -2, 'y': 48, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2017-09-15', 'x': -2, 'y': 60, 'fill': '#ebedf0'},
        {'count': 1, 'date': '2017-09-16', 'x': -2, 'y': 72, 'fill': '#c6e48b'},
        {'count': 3, 'date': '2017-09-17', 'x': -3, 'y': 0, 'fill': '#239a3b'},
        {'count': 1, 'date': '2017-09-18', 'x': -3, 'y': 12, 'fill': '#c6e48b'},
        {'count': 1, 'date': '2017-09-19', 'x': -3, 'y': 24, 'fill': '#c6e48b'},
        {'count': 2, 'date': '2017-09-20', 'x': -3, 'y': 36, 'fill': '#7bc96f'},
        {'count': 3, 'date': '2017-09-21', 'x': -3, 'y': 48, 'fill': '#239a3b'},
        {'count': 3, 'date': '2017-09-22', 'x': -3, 'y': 60, 'fill': '#239a3b'},
        {'count': 1, 'date': '2017-09-23', 'x': -3, 'y': 72, 'fill': '#c6e48b'},
        {'count': 0, 'date': '2017-09-24', 'x': -4, 'y': 0, 'fill': '#ebedf0'},
        {'count': 2, 'date': '2017-09-25', 'x': -4, 'y': 12, 'fill': '#7bc96f'},
        {'count': 0, 'date': '2017-09-26', 'x': -4, 'y': 24, 'fill': '#ebedf0'},
        {'count': 3, 'date': '2017-09-27', 'x': -4, 'y': 36, 'fill': '#239a3b'},
        {'count': 0, 'date': '2017-09-28', 'x': -4, 'y': 48, 'fill': '#ebedf0'},
        {'count': 1, 'date': '2017-09-29', 'x': -4, 'y': 60, 'fill': '#c6e48b'},
        {'count': 2, 'date': '2017-09-30', 'x': -4, 'y': 72, 'fill': '#7bc96f'},
        {'count': 2, 'date': '2017-10-01', 'x': -5, 'y': 0, 'fill': '#7bc96f'},
        {'count': 2, 'date': '2017-10-02', 'x': -5, 'y': 12, 'fill': '#7bc96f'},
        {'count': 1, 'date': '2017-10-03', 'x': -5, 'y': 24, 'fill': '#c6e48b'},
        {'count': 1, 'date': '2017-10-04', 'x': -5, 'y': 36, 'fill': '#c6e48b'},
        {'count': 3, 'date': '2017-10-05', 'x': -5, 'y': 48, 'fill': '#239a3b'},
        {'count': 2, 'date': '2017-10-06', 'x': -5, 'y': 60, 'fill': '#7bc96f'},
        {'count': 1, 'date': '2017-10-07', 'x': -5, 'y': 72, 'fill': '#c6e48b'},
        {'count': 0, 'date': '2017-10-08', 'x': -6, 'y': 0, 'fill': '#ebedf0'},
        {'count': 1, 'date': '2017-10-09', 'x': -6, 'y': 12, 'fill': '#c6e48b'},
        {'count': 2, 'date': '2017-10-10', 'x': -6, 'y': 24, 'fill': '#7bc96f'},
        {'count': 0, 'date': '2017-10-11', 'x': -6, 'y': 36, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2017-10-12', 'x': -6, 'y': 48, 'fill': '#ebedf0'},
        {'count': 1, 'date': '2017-10-13', 'x': -6, 'y': 60, 'fill': '#c6e48b'},
        {'count': 2, 'date': '2017-10-14', 'x': -6, 'y': 72, 'fill': '#7bc96f'},
        {'count': 1, 'date': '2017-10-15', 'x': -7, 'y': 0, 'fill': '#c6e48b'},
        {'count': 0, 'date': '2017-10-16', 'x': -7, 'y': 12, 'fill': '#ebedf0'},
        {'count': 1, 'date': '2017-10-17', 'x': -7, 'y': 24, 'fill': '#c6e48b'},
        {'count': 1, 'date': '2017-10-18', 'x': -7, 'y': 36, 'fill': '#c6e48b'},
        {'count': 1, 'date': '2017-10-19', 'x': -7, 'y': 48, 'fill': '#c6e48b'},
        {'count': 0, 'date': '2017-10-20', 'x': -7, 'y': 60, 'fill': '#ebedf0'},
        {'count': 1, 'date': '2017-10-21', 'x': -7, 'y': 72, 'fill': '#c6e48b'},
        {'count': 3, 'date': '2017-10-22', 'x': -8, 'y': 0, 'fill': '#239a3b'},
        {'count': 0, 'date': '2017-10-23', 'x': -8, 'y': 12, 'fill': '#ebedf0'},
        {'count': 1, 'date': '2017-10-24', 'x': -8, 'y': 24, 'fill': '#c6e48b'},
        {'count': 1, 'date': '2017-10-25', 'x': -8, 'y': 36, 'fill': '#c6e48b'},
        {'count': 0, 'date': '2017-10-26', 'x': -8, 'y': 48, 'fill': '#ebedf0'},
        {'count': 2, 'date': '2017-10-27', 'x': -8, 'y': 60, 'fill': '#7bc96f'},
        {'count': 0, 'date': '2017-10-28', 'x': -8, 'y': 72, 'fill': '#ebedf0'},
        {'count': 1, 'date': '2017-10-29', 'x': -9, 'y': 0, 'fill': '#c6e48b'},
        {'count': 2, 'date': '2017-10-30', 'x': -9, 'y': 12, 'fill': '#7bc96f'},
        {'count': 3, 'date': '2017-10-31', 'x': -9, 'y': 24, 'fill': '#239a3b'},
        {'count': 0, 'date': '2017-11-01', 'x': -9, 'y': 36, 'fill': '#ebedf0'},
        {'count': 1, 'date': '2017-11-02', 'x': -9, 'y': 48, 'fill': '#c6e48b'},
        {'count': 3, 'date': '2017-11-03', 'x': -9, 'y': 60, 'fill': '#239a3b'},
        {'count': 1, 'date': '2017-11-04', 'x': -9, 'y': 72, 'fill': '#c6e48b'},
        {'count': 0, 'date': '2017-11-05', 'x': -10, 'y': 0, 'fill': '#ebedf0'},
        {'count': 3, 'date': '2017-11-06', 'x': -10, 'y': 12, 'fill': '#239a3b'},
        {'count': 1, 'date': '2017-11-07', 'x': -10, 'y': 24, 'fill': '#c6e48b'},
        {'count': 2, 'date': '2017-11-08', 'x': -10, 'y': 36, 'fill': '#7bc96f'},
        {'count': 0, 'date': '2017-11-09', 'x': -10, 'y': 48, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2017-11-10', 'x': -10, 'y': 60, 'fill': '#ebedf0'},
        {'count': 2, 'date': '2017-11-11', 'x': -10, 'y': 72, 'fill': '#7bc96f'},
        {'count': 0, 'date': '2017-11-12', 'x': -11, 'y': 0, 'fill': '#ebedf0'},
        {'count': 2, 'date': '2017-11-13', 'x': -11, 'y': 12, 'fill': '#7bc96f'},
        {'count': 2, 'date': '2017-11-14', 'x': -11, 'y': 24, 'fill': '#7bc96f'},
        {'count': 2, 'date': '2017-11-15', 'x': -11, 'y': 36, 'fill': '#7bc96f'},
        {'count': 0, 'date': '2017-11-16', 'x': -11, 'y': 48, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2017-11-17', 'x': -11, 'y': 60, 'fill': '#ebedf0'},
        {'count': 1, 'date': '2017-11-18', 'x': -11, 'y': 72, 'fill': '#c6e48b'},
        {'count': 0, 'date': '2017-11-19', 'x': -12, 'y': 0, 'fill': '#ebedf0'},
        {'count': 1, 'date': '2017-11-20', 'x': -12, 'y': 12, 'fill': '#c6e48b'},
        {'count': 3, 'date': '2017-11-21', 'x': -12, 'y': 24, 'fill': '#239a3b'},
        {'count': 1, 'date': '2017-11-22', 'x': -12, 'y': 36, 'fill': '#c6e48b'},
        {'count': 2, 'date': '2017-11-23', 'x': -12, 'y': 48, 'fill': '#7bc96f'},
        {'count': 0, 'date': '2017-11-24', 'x': -12, 'y': 60, 'fill': '#ebedf0'},
        {'count': 1, 'date': '2017-11-25', 'x': -12, 'y': 72, 'fill': '#c6e48b'},
        {'count': 1, 'date': '2017-11-26', 'x': -13, 'y': 0, 'fill': '#c6e48b'},
        {'count': 2, 'date': '2017-11-27', 'x': -13, 'y': 12, 'fill': '#7bc96f'},
        {'count': 0, 'date': '2017-11-28', 'x': -13, 'y': 24, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2017-11-29', 'x': -13, 'y': 36, 'fill': '#ebedf0'},
        {'count': 1, 'date': '2017-11-30', 'x': -13, 'y': 48, 'fill': '#c6e48b'},
        {'count': 2, 'date': '2017-12-01', 'x': -13, 'y': 60, 'fill': '#7bc96f'},
        {'count': 0, 'date': '2017-12-02', 'x': -13, 'y': 72, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2017-12-03', 'x': -14, 'y': 0, 'fill': '#ebedf0'},
        {'count': 1, 'date': '2017-12-04', 'x': -14, 'y': 12, 'fill': '#c6e48b'},
        {'count': 2, 'date': '2017-12-05', 'x': -14, 'y': 24, 'fill': '#7bc96f'},
        {'count': 1, 'date': '2017-12-06', 'x': -14, 'y': 36, 'fill': '#c6e48b'},
        {'count': 2, 'date': '2017-12-07', 'x': -14, 'y': 48, 'fill': '#7bc96f'},
        {'count': 1, 'date': '2017-12-08', 'x': -14, 'y': 60, 'fill': '#c6e48b'},
        {'count': 0, 'date': '2017-12-09', 'x': -14, 'y': 72, 'fill': '#ebedf0'},
        {'count': 7, 'date': '2017-12-10', 'x': -15, 'y': 0, 'fill': '#196127'},
        {'count': 1, 'date': '2017-12-11', 'x': -15, 'y': 12, 'fill': '#c6e48b'},
        {'count': 1, 'date': '2017-12-12', 'x': -15, 'y': 24, 'fill': '#c6e48b'},
        {'count': 1, 'date': '2017-12-13', 'x': -15, 'y': 36, 'fill': '#c6e48b'},
        {'count': 0, 'date': '2017-12-14', 'x': -15, 'y': 48, 'fill': '#ebedf0'},
        {'count': 1, 'date': '2017-12-15', 'x': -15, 'y': 60, 'fill': '#c6e48b'},
        {'count': 0, 'date': '2017-12-16', 'x': -15, 'y': 72, 'fill': '#ebedf0'},
        {'count': 1, 'date': '2017-12-17', 'x': -16, 'y': 0, 'fill': '#c6e48b'},
        {'count': 1, 'date': '2017-12-18', 'x': -16, 'y': 12, 'fill': '#c6e48b'},
        {'count': 1, 'date': '2017-12-19', 'x': -16, 'y': 24, 'fill': '#c6e48b'},
        {'count': 1, 'date': '2017-12-20', 'x': -16, 'y': 36, 'fill': '#c6e48b'},
        {'count': 0, 'date': '2017-12-21', 'x': -16, 'y': 48, 'fill': '#ebedf0'},
        {'count': 1, 'date': '2017-12-22', 'x': -16, 'y': 60, 'fill': '#c6e48b'},
        {'count': 0, 'date': '2017-12-23', 'x': -16, 'y': 72, 'fill': '#ebedf0'},
        {'count': 1, 'date': '2017-12-24', 'x': -17, 'y': 0, 'fill': '#c6e48b'},
        {'count': 0, 'date': '2017-12-25', 'x': -17, 'y': 12, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2017-12-26', 'x': -17, 'y': 24, 'fill': '#ebedf0'},
        {'count': 1, 'date': '2017-12-27', 'x': -17, 'y': 36, 'fill': '#c6e48b'},
        {'count': 1, 'date': '2017-12-28', 'x': -17, 'y': 48, 'fill': '#c6e48b'},
        {'count': 0, 'date': '2017-12-29', 'x': -17, 'y': 60, 'fill': '#ebedf0'},
        {'count': 4, 'date': '2017-12-30', 'x': -17, 'y': 72, 'fill': '#196127'},
        {'count': 2, 'date': '2017-12-31', 'x': -18, 'y': 0, 'fill': '#7bc96f'},
        {'count': 2, 'date': '2018-01-01', 'x': -18, 'y': 12, 'fill': '#7bc96f'},
        {'count': 1, 'date': '2018-01-02', 'x': -18, 'y': 24, 'fill': '#c6e48b'},
        {'count': 2, 'date': '2018-01-03', 'x': -18, 'y': 36, 'fill': '#7bc96f'},
        {'count': 1, 'date': '2018-01-04', 'x': -18, 'y': 48, 'fill': '#c6e48b'},
        {'count': 4, 'date': '2018-01-05', 'x': -18, 'y': 60, 'fill': '#196127'},
        {'count': 3, 'date': '2018-01-06', 'x': -18, 'y': 72, 'fill': '#239a3b'},
        {'count': 7, 'date': '2018-01-07', 'x': -19, 'y': 0, 'fill': '#196127'},
        {'count': 0, 'date': '2018-01-08', 'x': -19, 'y': 12, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-01-09', 'x': -19, 'y': 24, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-01-10', 'x': -19, 'y': 36, 'fill': '#ebedf0'},
        {'count': 1, 'date': '2018-01-11', 'x': -19, 'y': 48, 'fill': '#c6e48b'},
        {'count': 0, 'date': '2018-01-12', 'x': -19, 'y': 60, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-01-13', 'x': -19, 'y': 72, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-01-14', 'x': -20, 'y': 0, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-01-15', 'x': -20, 'y': 12, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-01-16', 'x': -20, 'y': 24, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-01-17', 'x': -20, 'y': 36, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-01-18', 'x': -20, 'y': 48, 'fill': '#ebedf0'},
        {'count': 2, 'date': '2018-01-19', 'x': -20, 'y': 60, 'fill': '#7bc96f'},
        {'count': 2, 'date': '2018-01-20', 'x': -20, 'y': 72, 'fill': '#7bc96f'},
        {'count': 5, 'date': '2018-01-21', 'x': -21, 'y': 0, 'fill': '#196127'},
        {'count': 1, 'date': '2018-01-22', 'x': -21, 'y': 12, 'fill': '#c6e48b'},
        {'count': 0, 'date': '2018-01-23', 'x': -21, 'y': 24, 'fill': '#ebedf0'},
        {'count': 1, 'date': '2018-01-24', 'x': -21, 'y': 36, 'fill': '#c6e48b'},
        {'count': 1, 'date': '2018-01-25', 'x': -21, 'y': 48, 'fill': '#c6e48b'},
        {'count': 5, 'date': '2018-01-26', 'x': -21, 'y': 60, 'fill': '#196127'},
        {'count': 5, 'date': '2018-01-27', 'x': -21, 'y': 72, 'fill': '#196127'},
        {'count': 1, 'date': '2018-01-28', 'x': -22, 'y': 0, 'fill': '#c6e48b'},
        {'count': 2, 'date': '2018-01-29', 'x': -22, 'y': 12, 'fill': '#7bc96f'},
        {'count': 0, 'date': '2018-01-30', 'x': -22, 'y': 24, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-01-31', 'x': -22, 'y': 36, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-02-01', 'x': -22, 'y': 48, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-02-02', 'x': -22, 'y': 60, 'fill': '#ebedf0'},
        {'count': 1, 'date': '2018-02-03', 'x': -22, 'y': 72, 'fill': '#c6e48b'},
        {'count': 0, 'date': '2018-02-04', 'x': -23, 'y': 0, 'fill': '#ebedf0'},
        {'count': 3, 'date': '2018-02-05', 'x': -23, 'y': 12, 'fill': '#239a3b'},
        {'count': 3, 'date': '2018-02-06', 'x': -23, 'y': 24, 'fill': '#239a3b'},
        {'count': 1, 'date': '2018-02-07', 'x': -23, 'y': 36, 'fill': '#c6e48b'},
        {'count': 1, 'date': '2018-02-08', 'x': -23, 'y': 48, 'fill': '#c6e48b'},
        {'count': 1, 'date': '2018-02-09', 'x': -23, 'y': 60, 'fill': '#c6e48b'},
        {'count': 0, 'date': '2018-02-10', 'x': -23, 'y': 72, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-02-11', 'x': -24, 'y': 0, 'fill': '#ebedf0'},
        {'count': 2, 'date': '2018-02-12', 'x': -24, 'y': 12, 'fill': '#7bc96f'},
        {'count': 0, 'date': '2018-02-13', 'x': -24, 'y': 24, 'fill': '#ebedf0'},
        {'count': 3, 'date': '2018-02-14', 'x': -24, 'y': 36, 'fill': '#239a3b'},
        {'count': 1, 'date': '2018-02-15', 'x': -24, 'y': 48, 'fill': '#c6e48b'},
        {'count': 0, 'date': '2018-02-16', 'x': -24, 'y': 60, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-02-17', 'x': -24, 'y': 72, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-02-18', 'x': -25, 'y': 0, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-02-19', 'x': -25, 'y': 12, 'fill': '#ebedf0'},
        {'count': 1, 'date': '2018-02-20', 'x': -25, 'y': 24, 'fill': '#c6e48b'},
        {'count': 1, 'date': '2018-02-21', 'x': -25, 'y': 36, 'fill': '#c6e48b'},
        {'count': 3, 'date': '2018-02-22', 'x': -25, 'y': 48, 'fill': '#239a3b'},
        {'count': 2, 'date': '2018-02-23', 'x': -25, 'y': 60, 'fill': '#7bc96f'},
        {'count': 0, 'date': '2018-02-24', 'x': -25, 'y': 72, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-02-25', 'x': -26, 'y': 0, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-02-26', 'x': -26, 'y': 12, 'fill': '#ebedf0'},
        {'count': 2, 'date': '2018-02-27', 'x': -26, 'y': 24, 'fill': '#7bc96f'},
        {'count': 2, 'date': '2018-02-28', 'x': -26, 'y': 36, 'fill': '#7bc96f'},
        {'count': 2, 'date': '2018-03-01', 'x': -26, 'y': 48, 'fill': '#7bc96f'},
        {'count': 3, 'date': '2018-03-02', 'x': -26, 'y': 60, 'fill': '#239a3b'},
        {'count': 0, 'date': '2018-03-03', 'x': -26, 'y': 72, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-03-04', 'x': -27, 'y': 0, 'fill': '#ebedf0'},
        {'count': 1, 'date': '2018-03-05', 'x': -27, 'y': 12, 'fill': '#c6e48b'},
        {'count': 0, 'date': '2018-03-06', 'x': -27, 'y': 24, 'fill': '#ebedf0'},
        {'count': 1, 'date': '2018-03-07', 'x': -27, 'y': 36, 'fill': '#c6e48b'},
        {'count': 3, 'date': '2018-03-08', 'x': -27, 'y': 48, 'fill': '#239a3b'},
        {'count': 2, 'date': '2018-03-09', 'x': -27, 'y': 60, 'fill': '#7bc96f'},
        {'count': 0, 'date': '2018-03-10', 'x': -27, 'y': 72, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-03-11', 'x': -28, 'y': 0, 'fill': '#ebedf0'},
        {'count': 1, 'date': '2018-03-12', 'x': -28, 'y': 12, 'fill': '#c6e48b'},
        {'count': 1, 'date': '2018-03-13', 'x': -28, 'y': 24, 'fill': '#c6e48b'},
        {'count': 3, 'date': '2018-03-14', 'x': -28, 'y': 36, 'fill': '#239a3b'},
        {'count': 2, 'date': '2018-03-15', 'x': -28, 'y': 48, 'fill': '#7bc96f'},
        {'count': 3, 'date': '2018-03-16', 'x': -28, 'y': 60, 'fill': '#239a3b'},
        {'count': 0, 'date': '2018-03-17', 'x': -28, 'y': 72, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-03-18', 'x': -29, 'y': 0, 'fill': '#ebedf0'},
        {'count': 1, 'date': '2018-03-19', 'x': -29, 'y': 12, 'fill': '#c6e48b'},
        {'count': 2, 'date': '2018-03-20', 'x': -29, 'y': 24, 'fill': '#7bc96f'},
        {'count': 2, 'date': '2018-03-21', 'x': -29, 'y': 36, 'fill': '#7bc96f'},
        {'count': 0, 'date': '2018-03-22', 'x': -29, 'y': 48, 'fill': '#ebedf0'},
        {'count': 2, 'date': '2018-03-23', 'x': -29, 'y': 60, 'fill': '#7bc96f'},
        {'count': 0, 'date': '2018-03-24', 'x': -29, 'y': 72, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-03-25', 'x': -30, 'y': 0, 'fill': '#ebedf0'},
        {'count': 3, 'date': '2018-03-26', 'x': -30, 'y': 12, 'fill': '#239a3b'},
        {'count': 3, 'date': '2018-03-27', 'x': -30, 'y': 24, 'fill': '#239a3b'},
        {'count': 3, 'date': '2018-03-28', 'x': -30, 'y': 36, 'fill': '#239a3b'},
        {'count': 2, 'date': '2018-03-29', 'x': -30, 'y': 48, 'fill': '#7bc96f'},
        {'count': 3, 'date': '2018-03-30', 'x': -30, 'y': 60, 'fill': '#239a3b'},
        {'count': 0, 'date': '2018-03-31', 'x': -30, 'y': 72, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-04-01', 'x': -31, 'y': 0, 'fill': '#ebedf0'},
        {'count': 3, 'date': '2018-04-02', 'x': -31, 'y': 12, 'fill': '#239a3b'},
        {'count': 2, 'date': '2018-04-03', 'x': -31, 'y': 24, 'fill': '#7bc96f'},
        {'count': 2, 'date': '2018-04-04', 'x': -31, 'y': 36, 'fill': '#7bc96f'},
        {'count': 0, 'date': '2018-04-05', 'x': -31, 'y': 48, 'fill': '#ebedf0'},
        {'count': 3, 'date': '2018-04-06', 'x': -31, 'y': 60, 'fill': '#239a3b'},
        {'count': 0, 'date': '2018-04-07', 'x': -31, 'y': 72, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-04-08', 'x': -32, 'y': 0, 'fill': '#ebedf0'},
        {'count': 3, 'date': '2018-04-09', 'x': -32, 'y': 12, 'fill': '#239a3b'},
        {'count': 2, 'date': '2018-04-10', 'x': -32, 'y': 24, 'fill': '#7bc96f'},
        {'count': 3, 'date': '2018-04-11', 'x': -32, 'y': 36, 'fill': '#239a3b'},
        {'count': 0, 'date': '2018-04-12', 'x': -32, 'y': 48, 'fill': '#ebedf0'},
        {'count': 3, 'date': '2018-04-13', 'x': -32, 'y': 60, 'fill': '#239a3b'},
        {'count': 0, 'date': '2018-04-14', 'x': -32, 'y': 72, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-04-15', 'x': -33, 'y': 0, 'fill': '#ebedf0'},
        {'count': 2, 'date': '2018-04-16', 'x': -33, 'y': 12, 'fill': '#7bc96f'},
        {'count': 3, 'date': '2018-04-17', 'x': -33, 'y': 24, 'fill': '#239a3b'},
        {'count': 1, 'date': '2018-04-18', 'x': -33, 'y': 36, 'fill': '#c6e48b'},
        {'count': 2, 'date': '2018-04-19', 'x': -33, 'y': 48, 'fill': '#7bc96f'},
        {'count': 3, 'date': '2018-04-20', 'x': -33, 'y': 60, 'fill': '#239a3b'},
        {'count': 0, 'date': '2018-04-21', 'x': -33, 'y': 72, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-04-22', 'x': -34, 'y': 0, 'fill': '#ebedf0'},
        {'count': 1, 'date': '2018-04-23', 'x': -34, 'y': 12, 'fill': '#c6e48b'},
        {'count': 2, 'date': '2018-04-24', 'x': -34, 'y': 24, 'fill': '#7bc96f'},
        {'count': 3, 'date': '2018-04-25', 'x': -34, 'y': 36, 'fill': '#239a3b'},
        {'count': 2, 'date': '2018-04-26', 'x': -34, 'y': 48, 'fill': '#7bc96f'},
        {'count': 2, 'date': '2018-04-27', 'x': -34, 'y': 60, 'fill': '#7bc96f'},
        {'count': 0, 'date': '2018-04-28', 'x': -34, 'y': 72, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-04-29', 'x': -35, 'y': 0, 'fill': '#ebedf0'},
        {'count': 3, 'date': '2018-04-30', 'x': -35, 'y': 12, 'fill': '#239a3b'},
        {'count': 2, 'date': '2018-05-01', 'x': -35, 'y': 24, 'fill': '#7bc96f'},
        {'count': 0, 'date': '2018-05-02', 'x': -35, 'y': 36, 'fill': '#ebedf0'},
        {'count': 2, 'date': '2018-05-03', 'x': -35, 'y': 48, 'fill': '#7bc96f'},
        {'count': 2, 'date': '2018-05-04', 'x': -35, 'y': 60, 'fill': '#7bc96f'},
        {'count': 3, 'date': '2018-05-05', 'x': -35, 'y': 72, 'fill': '#239a3b'},
        {'count': 0, 'date': '2018-05-06', 'x': -36, 'y': 0, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-05-07', 'x': -36, 'y': 12, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-05-08', 'x': -36, 'y': 24, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-05-09', 'x': -36, 'y': 36, 'fill': '#ebedf0'},
        {'count': 4, 'date': '2018-05-10', 'x': -36, 'y': 48, 'fill': '#196127'},
        {'count': 0, 'date': '2018-05-11', 'x': -36, 'y': 60, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-05-12', 'x': -36, 'y': 72, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-05-13', 'x': -37, 'y': 0, 'fill': '#ebedf0'},
        {'count': 2, 'date': '2018-05-14', 'x': -37, 'y': 12, 'fill': '#7bc96f'},
        {'count': 0, 'date': '2018-05-15', 'x': -37, 'y': 24, 'fill': '#ebedf0'},
        {'count': 1, 'date': '2018-05-16', 'x': -37, 'y': 36, 'fill': '#c6e48b'},
        {'count': 2, 'date': '2018-05-17', 'x': -37, 'y': 48, 'fill': '#7bc96f'},
        {'count': 0, 'date': '2018-05-18', 'x': -37, 'y': 60, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-05-19', 'x': -37, 'y': 72, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-05-20', 'x': -38, 'y': 0, 'fill': '#ebedf0'},
        {'count': 4, 'date': '2018-05-21', 'x': -38, 'y': 12, 'fill': '#196127'},
        {'count': 0, 'date': '2018-05-22', 'x': -38, 'y': 24, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-05-23', 'x': -38, 'y': 36, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-05-24', 'x': -38, 'y': 48, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-05-25', 'x': -38, 'y': 60, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-05-26', 'x': -38, 'y': 72, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-05-27', 'x': -39, 'y': 0, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-05-28', 'x': -39, 'y': 12, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-05-29', 'x': -39, 'y': 24, 'fill': '#ebedf0'},
        {'count': 0, 'date': '2018-05-30', 'x': -39, 'y': 36, 'fill': '#ebedf0'},
        {'count': 4, 'date': '2018-05-31', 'x': -39, 'y': 48, 'fill': '#196127'}
    ],
    'colormap': {
        '#239a3b': range(3, 4),
        '#7bc96f': range(2, 3),
        '#ebedf0': range(0, 1),
        '#196127': range(4, 8),
        '#c6e48b': range(1, 2)
    }
}

mock_response_fd = StringIO("foobar")


def _mock_response(req):
    if req.get_full_url() == "https://github.com/users/404/contributions":
        resp = urllib.response.addinfourl(
            mock_response_fd,
            "mock message",
            req.get_full_url()
        )
        resp.code = 404
        resp.msg = "Not Found"
        return resp
    else:
        resp = urllib.response.addinfourl(
            mock_response_fd,
            "mock message",
            req.get_full_url()
        )
        resp.code = 200
        resp.msg = "OK"
        return resp


class MockHTTPHandler(urllib.request.HTTPSHandler):
    """Mock handler to load graph data from the filesystem."""

    def https_open(self, req):
        return self.http_open(req)

    @staticmethod
    def http_open(req):
        return _mock_response(req)


class TestFetchMethod(unittest.TestCase):
    """Tests for the Graph.fetch() method."""

    def setUp(self):
        mock_opener = urllib.request.build_opener(MockHTTPHandler)
        urllib.request.install_opener(mock_opener)

    def tearDown(self):
        urllib.request._opener = None

    def test_fetch_valid_graph(self):
        global mock_response_fd

        with open(CONTRIB_HTML, 'r') as mock_response_fd:
            g = graph.Graph('200')
            g.fetch()

        self.assertEqual(g.data, VALID_GRAPH_REFERENCE_DATA)

    def test_fetch_garbage_graph(self):
        """Check for ValueError if data is not an SVG file."""

        global mock_response_fd

        with open(GARBAGE_HTML, 'r') as mock_response_fd:
            g = graph.Graph('user')
            with self.assertRaises(ValueError) as cm:
                g.fetch()

        exc = cm.exception
        self.assertEqual('Expected svg, got html', str(exc))

    def test_fetch_wrong_svg_class(self):
        """Check for ValueError if SVG has wrong class attribute."""

        global mock_response_fd

        with open(CLASS_HTML, 'r') as mock_response_fd:
            g = graph.Graph('user')
            with self.assertRaises(ValueError) as cm:
                g.fetch()

        exc = cm.exception
        self.assertEqual(
            'Expected class js-calendar-graph-svg, got foo',
            str(exc)
        )

    def test_fetch_short_graph(self):
        """Check for ValueError if there is not enough data in the graph."""

        global mock_response_fd

        with open(SHORT_HTML, 'r') as mock_response_fd:
            g = graph.Graph('user')
            with self.assertRaises(ValueError) as cm:
                g.fetch()

        exc = cm.exception
        self.assertEqual('Too few data points in graph: 14 < 365', str(exc))

    def test_fetch_404(self):
        """Check for HTTPError if response is 404."""

        global mock_response_fd

        mock_response_fd = StringIO("mock 404")
        g = graph.Graph('404')
        with self.assertRaises(HTTPError) as cm:
            g.fetch()

        exc = cm.exception
        self.assertEqual(exc.code, 404)


if __name__ == '__main__':
    unittest.main()
