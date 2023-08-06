##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
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
"""Persistent Local Permissions
"""
__docformat__ = 'restructuredtext'

from persistent import Persistent
from zope.component import adapter
from zope.interface.interfaces import IRegistered, IUnregistered
from zope.i18nmessageid import MessageFactory
from zope.interface import implementer
from zope.location import Location
from zope.security.interfaces import IPermission

_ = MessageFactory('zope')

NULL_ID = _(u'<permission not activated>')

@implementer(IPermission)
class LocalPermission(Persistent, Location):

    def __init__(self, title=u'', description=u''):
        self.id = NULL_ID
        self.title = title
        self.description = description


@adapter(IPermission, IRegistered)
def setIdOnActivation(permission, event):
    """Set the permission id upon registration activation.

    Let's see how this notifier can be used. First we need to create an event
    using the permission instance and a registration stub:

    >>> class Registration(object):
    ...     def __init__(self, obj, name):
    ...         self.component = obj
    ...         self.name = name

    >>> perm1 = LocalPermission('Permission 1', 'A first permission')
    >>> print(perm1.id)
    <permission not activated>

    >>> import zope.interface.interfaces
    >>> event = zope.interface.interfaces.Registered(
    ...     Registration(perm1, 'perm1'))

    Now we pass the event into this function, and the id of the permission
    should be set to 'perm1'.

    >>> setIdOnActivation(perm1, event)
    >>> perm1.id
    'perm1'
    """
    permission.id = event.object.name


@adapter(IPermission, IUnregistered)
def unsetIdOnDeactivation(permission, event):
    """Unset the permission id up registration deactivation.

    Let's see how this notifier can be used. First we need to create an event
    using the permission instance and a registration stub:

    >>> class Registration(object):
    ...     def __init__(self, obj, name):
    ...         self.component = obj
    ...         self.name = name

    >>> perm1 = LocalPermission('Permission 1', 'A first permission')
    >>> perm1.id = 'perm1'

    >>> import zope.interface.interfaces
    >>> event = zope.interface.interfaces.Unregistered(
    ...     Registration(perm1, 'perm1'))

    Now we pass the event into this function, and the id of the permission
    should be set to NULL_ID.

    >>> unsetIdOnDeactivation(perm1, event)
    >>> print(perm1.id)
    <permission not activated>
    """
    permission.id = NULL_ID
