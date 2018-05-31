#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# SPDX-License-Identifier:     MIT

import unittest
import urllib.request
from io import StringIO

def _mock_response_200(req):
    if req.get_full_url() == "http://example.com":
        resp = urllib.response.addinfourl(StringIO("mock file"), "mock message", req.get_full_url())
        resp.code = 200
        resp.msg = "OK"
        return resp

def _mock_response_404(req):
    if req.get_full_url() == "http://example.com":
        resp = urllib.response.addinfourl(StringIO("mock file"), "mock message", req.get_full_url())
        resp.code = 404
        resp.msg = "OK"
        return resp

class MockHTTPHandler(urllib.request.HTTPHandler):

    def http_open(self, req):
        return _mock_response_404(req)


class TestFetchMethod(unittest.TestCase):
    
    def test_fetch_404(self):
        mock_opener = urllib.request.build_opener(MockHTTPHandler)
        urllib.request.install_opener(mock_opener)
        response=urllib.request.urlopen("http://example.com")
        print(response.read())
        print(response.code)
        print(response.msg)
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()

