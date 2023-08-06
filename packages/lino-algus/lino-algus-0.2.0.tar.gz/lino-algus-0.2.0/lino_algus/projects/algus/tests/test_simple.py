# -*- coding: utf-8 -*-
# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
You can run only these tests by issuing::

  $ python setup.py test -s tests.DemoTests.test_algus

Or::

  $ go algus
  $ cd lino_algus/projects/algus
  $ python manage.py test tests.test_simple



"""

from __future__ import unicode_literals
from __future__ import print_function

from django.core.exceptions import ValidationError
from lino.utils.djangotest import RemoteAuthTestCase
from lino.api import rt


def create(m, **kwargs):
    obj = m(**kwargs)
    obj.full_clean()
    obj.save()
    return obj
    

class SimpleTests(RemoteAuthTestCase):
    maxDiff = None

    def test01(self):
        User = rt.models.users.User
        UserTypes = rt.models.users.UserTypes
        Product = rt.models.lets.Product
        
        robin = create(User, username='robin',
                       user_type=UserTypes.admin,
                       language="en")

        foo = create(Product, name='Foo')

