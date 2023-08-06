# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)


"""
Lino Algus extension of :mod:`lino.modlib.users`.

.. autosummary::
   :toctree:

    models
    desktop
    fixtures.demo
    fixtures.demo2

"""

from lino.modlib.users import Plugin


class Plugin(Plugin):
   
    extends_models = ['User']

