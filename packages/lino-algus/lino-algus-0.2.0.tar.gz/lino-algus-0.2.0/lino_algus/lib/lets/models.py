# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)
"""Database models for this plugin."""

from django.db import models
from lino.api import dd
from lino.utils import join_elems
from etgen.html import E
from lino.core.actors import qs2summary
from lino.utils.mldbc.mixins import BabelNamed

class Place(BabelNamed):
    pass


class Product(BabelNamed):

    providers = models.ManyToManyField(
        'users.User', verbose_name="Offered by",
        through='lets.Offer', related_name='offered_products')
    customers = models.ManyToManyField(
        'users.User', verbose_name="Wanted by",
        through='lets.Demand', related_name='wanted_products')

    @dd.displayfield("Offered by")
    def offered_by(self, ar):
        if ar is None:
            return ''
        return qs2summary(ar, self.providers.all())

    @dd.displayfield("Wanted by")
    def wanted_by(self, ar):
        if ar is None:
            return ''
        return qs2summary(ar, self.customers.all())


@dd.python_2_unicode_compatible
class Offer(dd.Model):
    provider = dd.ForeignKey('users.User')
    product = dd.ForeignKey(Product)
    valid_until = models.DateField(blank=True, null=True)

    def __str__(self):
        return "%s offered by %s" % (self.product, self.provider)


@dd.python_2_unicode_compatible
class Demand(dd.Model):
    customer = dd.ForeignKey('users.User')
    product = dd.ForeignKey(Product)

    def __str__(self):
        return "%s (%s)" % (self.product, self.customer)


