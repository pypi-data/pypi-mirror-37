#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `dappy` package."""


import unittest

from dappy import API, Endpoint
from dappy.methods import GET, POST


class TestDappy(unittest.TestCase):
    """Tests for `dappy` package."""

    def setUp(self):
        self.TestAPI = API('jsonplaceholder.typicode.com', [
            Endpoint('posts', '/posts', methods=[GET, POST])
        ])

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_get(self):
        self.assertTrue(self.TestAPI.posts.get() is not None)

    def test_post(self):
        self.assertTrue(self.TestAPI.posts.post({}) is not None)
