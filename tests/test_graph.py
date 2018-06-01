#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier:     MIT

import os
import unittest
import urllib.request
from urllib.error import HTTPError
from io import StringIO

from pointilist import graph

CONTRIB_HTML = os.path.dirname(os.path.realpath(__file__)) \
        + '/static/contributions.html'

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

    def https_open(self, req):
        return self.http_open(req)

    def http_open(self, req):
        return _mock_response(req)


class TestFetchMethod(unittest.TestCase):

    def setUp(self):
        mock_opener = urllib.request.build_opener(MockHTTPHandler)
        urllib.request.install_opener(mock_opener)

    def tearDown(self):
        urllib.request._opener = None

    def test_fetch_valid_graph(self):
        global mock_response_fd

        with open(CONTRIB_HTML, 'r') as mock_response_fd:
            g = graph.Graph('200')
            ret = g.fetch()

        self.assertTrue(False)

    def test_fetch_404(self):
        global mock_response_fd

        mock_response_fd = StringIO("mock 404")
        g = graph.Graph('404')
        with self.assertRaises(HTTPError) as cm:
            g.fetch()

        exc = cm.exception
        self.assertEqual(exc.code, 404)


if __name__ == '__main__':
    unittest.main()
