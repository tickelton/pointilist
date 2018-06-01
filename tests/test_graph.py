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

    @unittest.skip("not implemented, yet")
    def test_fetch_valid_graph(self):
        global mock_response_fd

        with open(CONTRIB_HTML, 'r') as mock_response_fd:
            g = graph.Graph('200')
            ret = g.fetch()

        self.assertTrue(False)

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
