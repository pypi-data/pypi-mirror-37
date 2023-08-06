##############################################################################
#
# Copyright (c) 2004 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Tests for zope.localpermission.
"""
import unittest
import doctest

from zope.testing.cleanup import CleanUp

import zope.app.localpermission

class TestConfiguration(CleanUp, unittest.TestCase):

    def test_configuration(self):
        from zope.configuration import xmlconfig
        xmlconfig.file('configure.zcml', package=zope.app.localpermission)

def test_suite():
    return unittest.TestSuite((
        doctest.DocTestSuite('zope.app.localpermission.permission'),
        unittest.defaultTestLoader.loadTestsFromName(__name__),
        ))
