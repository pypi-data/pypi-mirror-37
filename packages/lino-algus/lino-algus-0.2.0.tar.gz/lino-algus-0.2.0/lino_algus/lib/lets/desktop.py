# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)

from django.db.models import Q
from lino.api import dd


class Places(dd.Table):
    model = 'lets.Place'

class Products(dd.Table):
    model = 'lets.Product'
    order_by = ['name']

    detail_layout = """
    id name
    OffersByProduct DemandsByProduct
    """

    column_names = 'id name providers customers'


class ActiveProducts(Products):

    label = "Active products"
    column_names = 'name offered_by wanted_by'

    @classmethod
    def get_request_queryset(cls, ar):
        # add filter condition to the queryset so that only active
        # products are shown, i.e. for which there is at least one
        # offer or one demand.
        qs = super(ActiveProducts, cls).get_request_queryset(ar)
        qs = qs.filter(Q(offer__isnull=False) | Q(demand__isnull=False))
        qs = qs.distinct()
        return qs


class Offers(dd.Table):
    model = 'lets.Offer'
    column_names = "id provider product valid_until *"


class OffersByUser(Offers):
    master_key = 'provider'


class OffersByProduct(Offers):
    master_key = 'product'


class Demands(dd.Table):
    model = 'lets.Demand'


class DemandsByUser(Demands):
    master_key = 'customer'


class DemandsByProduct(Demands):
    master_key = 'product'

