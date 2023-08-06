# -*- coding: UTF-8 -*-
# Copyright 2016-2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""
.. autosummary::
   :toctree:

    models
    desktop


"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."
    verbose_name = _("Local Exchange")

    def setup_main_menu(self, site, profile, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('lets.Offers')
        m.add_action('lets.Demands')

    def get_dashboard_items(self, user):
        yield self.site.models.lets.ActiveProducts

