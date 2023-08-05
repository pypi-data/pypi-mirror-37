#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import paspas.generator

class GeneratorTest(unittest.TestCase):
    site = 'google'
    user = 'bob'
    master = 'secret'
    
    def test_default(self):
        self.assertEqual(paspas.generator.generate(self.site, self.user, self.master), 'NjlmNzJkYzFiMGQzYzQ2YzZlODk4M2JlMTQ0NDFjMzM0MzQ3YWM3MDEzNmFkY2I3NmVhMjkwNzQ0ODczYjA0YmYzZGFlNTRjZTFlN2UzYjBjNWNmOWY2N2Y3ZmMzZjhhODBkYzcxYTk4MTg5ZDBlYWQwYWMyOGNjNTRmZTI3MDc=');

    def test_max_length(self):
        self.assertEqual(paspas.generator.generate(self.site, self.user, self.master, 10), 'NjlmNzJkYz')

    def test_unavailable_char(self):
        self.assertEqual(paspas.generator.generate(self.site, self.user, self.master, 10, 'Nj'), 'lmzJkYzFiM')

if __name__ == '__main__':
    unittest.main()
