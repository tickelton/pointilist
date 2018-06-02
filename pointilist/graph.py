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


class Graph:
    """Object that represents a user's github contribution graph."""

    data = {}

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

    def _create_colormap(self):
        max_count = int(max(self.data['rects'], key=lambda r: r['count'])['count'])
        thresholds = [int(max_count*x) for x in [0.25, 0.5, 0.75]]
        # #ebedf0 = 0
        # c6e48b = 1 <= x <= max/6
        # 7bc96f = max/6 < x <= max/3
        # 239a3b = max/3 < x <= max/2
        # #196127 = x > max/2
        print(max_count, thresholds)

    def _parse_graph_data(self, graph_data):
        root = ET.fromstring(graph_data)

        self.data['rects'] = [
            {
                'date': rect.get('data-date'),
                'count': rect.get('data-count'),
                'fill': rect.get('fill'),
                'x': rect.get('x'),
                'y': rect.get('y')
            } for rect in root.iter('rect') if rect.get('class') == 'day'
        ]

        self.data['months'] = [
            {
                'month': text.text,
                'x': text.get('x'),
                'y': text.get('y')
            } for text in root.iter('text') if text.get('class') == 'month'
        ]

        self.data['wdays'] = [
            {
                'wday': text.text,
                'display': text.get('style') != "display: none;",
                'x': text.get('dx'),
                'y': text.get('dy')
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
