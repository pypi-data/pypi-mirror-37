# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""Default data migrator for Lino Algus.


"""

from django.conf import settings
from lino.api import dd, rt
from lino.utils.dpy import Migrator, override

class Migrator(Migrator):
    """The standard migrator for Lino Algus.

    This is used because
    :class:`lino_algus.projects.algus.settings.Site` has
    :attr:`migration_class <lino.core.site.Site.migration_class>` set
    to ``"lino_algus.lib.algus.migrate.Migrator"``.

    """
    def migrate_from_0_0_1(self, globals_dict):
        # do something here
        return '0.0.2'

