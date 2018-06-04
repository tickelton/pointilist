#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier:     MIT

"""
    Handles the interaction with github contribution graph data.

    :copyright: © 2018, tickelton <tickelton@gmail.com>.
    :license: MIT, see LICENSE for details.
"""

import random
import logging
import urllib.request
import xml.etree.ElementTree as ET

FILL_DEFAULT = ['#ebedf0', '#c6e48b', '#7bc96f', '#239a3b', '#196127']
RANDOM_BIAS = [0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 4]


class Graph:
    """Object that represents a user's github contribution graph."""

    def __init__(self, username):
        self.username = username
        self.data = {}

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

    def _get_fill(self, idx, count):
        try:
            return next(
                filter(lambda x: x['count'] in count, self.data['rects'])
            )['fill']
        except StopIteration:
            logging.info("Using default fill for %s.", count)
            return FILL_DEFAULT[idx]

    def _create_colormap(self):
        """ Creates a map that determines the color
            to be used for a given commit count according
            to the following scheme:

            count == 0                     => color0 (#ebedf0)
            1 <= count <= max_count/6      => color1 (#c6e48b)
            max_count/6 < x <= max_count/3 => color2 (#7bc96f)
            max_count/3 < x <= max_count/2 => color3 (#239a3b)
            count > max_count/2            => color4 (#1961270
        """

        max_count = max(self.data['rects'], key=lambda r: r['count'])['count']
        ranges_list = [
            [
                int(max_count/x[0])+1,
                int(max_count/x[1])+1
            ] for x in [[6, 3], [3, 2], [2, 1]]
        ]
        ranges_list = [[0, 1]] + [[1, ranges_list[0][0]]] + ranges_list

        self.data['colormap'] = [
            {
                'fill': self._get_fill(
                    i,
                    range(
                        ranges_list[i][0],
                        ranges_list[i][1]
                    )
                ),
                'range': range(
                    ranges_list[i][0],
                    ranges_list[i][1]
                )
            } for i in range(0, 5)
        ]

    def _parse_graph_data(self, graph_data):
        root = ET.fromstring(graph_data)

        self.data['rects'] = [
            {
                'date': rect.get('data-date'),
                'count': int(rect.get('data-count')),
                'fill': rect.get('fill'),
                'x': int(rect.get('x')),
                'y': int(rect.get('y'))
            } for rect in root.iter('rect') if rect.get('class') == 'day'
        ]

        self.data['months'] = [
            {
                'month': text.text,
                'x': int(text.get('x')),
                'y': int(text.get('y'))
            } for text in root.iter('text') if text.get('class') == 'month'
        ]

        self.data['wdays'] = [
            {
                'wday': text.text,
                'display': text.get('style') != "display: none;",
                'x': int(text.get('dx')),
                'y': int(text.get('dy'))
            } for text in root.iter('text') if text.get('class') == 'wday'
        ]

        self._create_colormap()

    def fetch(self):
        """Retrieves contribution data from github."""

        url = 'https://github.com/users/' + self.username + '/contributions'
        page = urllib.request.urlopen(url)
        graph_data = page.read()

        self._graph_data_valid(graph_data)
        self._parse_graph_data(graph_data)

    def fill(self):
        """Fills contribution graph with random data."""

        if self.data == {}:
            raise ValueError(
                'Graph data empty; maybe you need to call fetch() first?'
            )

        random.seed()
        self.data['commits'] = []
        for rect in self.data['rects']:
            if rect['count'] == 0:
                i = RANDOM_BIAS[random.randint(0, len(RANDOM_BIAS)-1)]
                self.data['commits'].append(
                    {
                        'date': rect['date'],
                        'count': self.data['colormap'][i]['range'].start
                    }
                )
