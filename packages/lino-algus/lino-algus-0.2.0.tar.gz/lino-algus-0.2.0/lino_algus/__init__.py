# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""This is the main module of Lino Algus.

.. autosummary::
   :toctree:

   lib
   projects


"""

from os.path import join, dirname
fn = join(dirname(__file__), 'setup_info.py')
exec(compile(open(fn, "rb").read(), fn, 'exec'))
# above line is equivalent to "execfile(filename)", except that it
# works also in Python 3

__version__ = SETUP_INFO.get('version')

intersphinx_urls = dict(docs="http://algus.lino-framework.org")
srcref_url = 'https://github.com/lino-framework/algus/blob/master/%s'
doc_trees = ['docs']

