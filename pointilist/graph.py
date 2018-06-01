#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier:     MIT

"""
    Handles the interaction with github contribution graph data.

    :copyright: © 2018, tickelton <tickelton@gmail.com>.
    :license: MIT, see LICENSE for details.
"""

import urllib.request
import xml.etree.ElementTree as ET

#graph_data = {
#        'rects': [
#            {
#                'date': '2017-05-28',
#                'count': 3,
#                'fill': '#239a3b',
#                'y': 0,
#                'x': 13
#            },
#            {
#                'date': '2017-05-29',
#                'count': 3,
#                'fill': '#239a3b',
#                'y': 12,
#                'x': 13
#            },
#            ...
#        ],
#        'months': [
#            {
#                'month': 'June',
#                'x': 25,
#                'y': 10
#            },
#            {
#                'month': 'Jul',
#                'x': 73,
#                'y': 10
#            },
#            ...
#        ],
#        'wdays': [
#            {
#                'wday': 'Sun',
#                'display': False,
#                'x': -14,
#                'y': 8
#            },
#            {
#                'wday': 'Mon',
#                'display': True,
#                'x': -14,
#                'y': 20
#            },
#            ...
#        ]
#    }


class Graph:
    """Object that represents a user's github contribution graph."""

    def __init__(self, username):
        self.username = username

    @staticmethod
    def _graph_data_valid(data):
        """Makes sure input data looks like a valid contribution graph."""

        rect_count = 0
        root = ET.fromstring(data)

        # check if data is an SVG file
        if root.tag != 'svg':
            raise ValueError('Expected svg, got {}'.format(root.tag))

        # check if SVG class is correct
        if root.get('class') != 'js-calendar-graph-svg':
            raise ValueError(
                'Expected class js-calendar-graph-svg, got {}'.format(
                    root.get('class')
                )
            )

        # check if there are at least 365 days worth of data
        for rect in root.iter('rect'):
            if rect.get('class') == 'day':
                rect_count += 1
        if rect_count < 365:
            raise ValueError(
                'Too few data points in graph: {} < 365'.format(rect_count)
            )

    def fetch(self):
        """Retrieves contribution data from github."""

        url = 'https://github.com/users/' + self.username + '/contributions'
        page = urllib.request.urlopen(url)
        graph_data = page.read()

        self._graph_data_valid(graph_data)
