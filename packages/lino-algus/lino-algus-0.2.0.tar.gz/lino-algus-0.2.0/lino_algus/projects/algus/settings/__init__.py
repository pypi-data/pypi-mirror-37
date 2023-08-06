# -*- coding: UTF-8 -*-
# Copyright 2016-2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""

.. autosummary::
   :toctree:

   doctests
   demo
   memory
   fixtures



"""

from __future__ import print_function
from __future__ import unicode_literals

from lino.projects.std.settings import *


class Site(Site):

    verbose_name = "Lino Algus"
    version = '0.0.1'
    url = "http://algus.lino-framework.org/"
    demo_fixtures = ['std', 'demo', 'demo2']
    user_types_module = 'lino_algus.lib.algus.user_types'
    migration_class = 'lino_algus.lib.algus.migrate.Migrator'

    def get_installed_apps(self):
        """Implements :meth:`lino.core.site.Site.get_installed_apps`.

        """
        yield super(Site, self).get_installed_apps()
        yield 'lino_algus.lib.users'
        yield 'lino_algus.lib.lets'
        yield 'lino_algus.lib.algus'
        yield 'lino.modlib.export_excel'
        yield 'lino.modlib.tinymce'
        yield 'lino.modlib.weasyprint'
        yield 'lino_xl.lib.appypod'


    def setup_quicklinks(self, user, tb):
        super(Site, self).setup_quicklinks(user, tb)
        tb.add_action('lets.Products')


# the following line should not be active in a checked-in version
# DATABASES['default']['NAME'] = ':memory:'

USE_TZ = True
TIME_ZONE = 'UTC'

