##############################################################################
#
# Copyright (c) 2001, 2002 Zope Foundation and Contributors.
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
"""Unit tests for Dependable class.
"""

import unittest

from zope.annotation.attribute import AttributeAnnotations
from zope.location.interfaces import ILocationInfo
from zope.interface import implementer, verify, directlyProvides
from zope.lifecycleevent import ObjectRemovedEvent

from zope.location.interfaces import ILocationInfo

from zope.testing.cleanup import CleanUp

import zope.app.dependable
from zope.app.dependable.dependency import CheckDependency
from zope.app.dependable.interfaces import IDependable, DependencyError


class C(object):
    pass


@implementer(IDependable, ILocationInfo)
class DummyObject(object):

    def dependents(self):
        return ['dependency1', 'dependency2']

    def getPath(self):
        return '/dummy-object'


class TestDependable(unittest.TestCase):

    def factory(self, obj=None):
        from zope.app.dependable import Dependable
        return Dependable(obj if obj is not None else AttributeAnnotations(C()))

    def testVerifyInterface(self):
        object = self.factory()
        verify.verifyObject(IDependable, object)

    def testBasic(self):
        dependable = self.factory()
        self.assertFalse(dependable.dependents())
        dependable.addDependent('/a/b')
        dependable.addDependent('/c/d')
        dependable.addDependent('/c/e')
        dependable.addDependent('/c/d')
        dependents = list(dependable.dependents())
        dependents.sort()
        self.assertEqual(dependents, ['/a/b', '/c/d', '/c/e'])
        dependable.removeDependent('/c/d')
        dependents = list(dependable.dependents())
        dependents.sort()
        self.assertEqual(dependents, ['/a/b', '/c/e'])
        dependable.removeDependent('/c/d')
        dependents = list(dependable.dependents())
        dependents.sort()
        self.assertEqual(dependents, ['/a/b', '/c/e'])

    def testRelativeAbsolute(self):
        obj = self.factory()
        # Hack the object to have a parent path
        obj.pp = "/a/"
        obj.pplen = len(obj.pp)
        obj.addDependent("foo")
        self.assertEqual(obj.dependents(), ("/a/foo",))
        obj.removeDependent("/a/foo")
        self.assertEqual(obj.dependents(), ())
        obj.addDependent("/a/bar")
        self.assertEqual(obj.dependents(), ("/a/bar",))
        obj.removeDependent("bar")
        self.assertEqual(obj.dependents(), ())

    def testCheckDependency(self):
        obj = DummyObject()
        parent = object()
        event = ObjectRemovedEvent(obj, parent, 'oldName')
        self.assertRaises(DependencyError, CheckDependency, event)

    def testWithParent(self):
        grandparent = C()
        grandparent.__name__ = 'root'

        parent = C()
        parent.__name__ = 'parent'
        parent.__parent__ = grandparent

        obj = AttributeAnnotations(parent)
        obj.__name__ = 'obj'

        from zope.traversing.api import getPath

        # If we can't get the parent path, it's just /
        dependable = self.factory(obj)
        self.assertEqual('/', dependable.pp)

        # If we can, it's whatever it reported, always with a
        # trailing /
        directlyProvides(parent, ILocationInfo)
        parent.getPath = lambda: '/root/parent'
        dependable = self.factory(obj)
        self.assertEqual('/root/parent/', dependable.pp)

        parent.getPath = lambda: '/root/parent/'
        dependable = self.factory(obj)
        self.assertEqual('/root/parent/', dependable.pp)


        dependable.addDependent('/root/parent/sibling/nephew')
        dependents = list(dependable.dependents())
        self.assertEqual(dependents, ['/root/parent/sibling/nephew'])


class TestConfiguration(CleanUp, unittest.TestCase):

    def test_configuration(self):
        from zope.configuration import xmlconfig
        xmlconfig.file('configure.zcml', package=zope.app.dependable)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)


if __name__=='__main__': # pragma: no cover
    unittest.main(defaultTest='test_suite')
