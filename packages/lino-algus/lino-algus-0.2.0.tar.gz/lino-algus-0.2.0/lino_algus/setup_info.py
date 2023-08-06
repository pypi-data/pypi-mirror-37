# -*- coding: UTF-8 -*-
# Copyright 2016-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

SETUP_INFO = dict(
    name='lino-algus',
    version='0.2.0',
    install_requires=['lino-xl'],
    description=("A template for new Lino applications"),
    author='Luc Saffre',
    author_email='luc@lino-framework.org',
    url="http://algus.lino-framework.org/",
    # license='GNU Affero General Public License v3',
    license='BSD License',
    test_suite='tests')


SETUP_INFO.update(long_description="""

A project which you can use as template for writing your own `Lino
<http://www.lino-framework.org/>`_ application.

Basic use is as follows:

- Find a short one-word name for your application, for example "Lino
  Example".

- Download and unzip a snapshot of this repository to a directory
  named "~/projects/example".

- In your project directory, rename all files and directories
  containing "algus" in their name to "example"::

       $ git mv lino_algus lino_example
       $ git mv lino_algus/lib/algus lino_example/lib/example
       $ ...

- In all your files (`.py`, `.rst`, `.html`), replace all occurences
  of "algus" by "example" (and "Algus" by "Example").

Note: "algus" is the Estonian word for "start". We did not name this
template "Lino Start" because the word "start" is more likely to occur
in variable names or text which is not related to the projet name.

""")

SETUP_INFO.update(classifiers="""
Programming Language :: Python
Programming Language :: Python :: 2
Development Status :: 4 - Beta
Environment :: Web Environment
Framework :: Django
Intended Audience :: Developers
Intended Audience :: System Administrators
Intended Audience :: Information Technology
Intended Audience :: Customer Service
License :: OSI Approved :: {license}
Operating System :: OS Independent
Topic :: Software Development :: Bug Tracking
""".format(**SETUP_INFO).strip().splitlines())
SETUP_INFO.update(packages=[
    'lino_algus',
    'lino_algus.lib',
    'lino_algus.lib.algus',
    'lino_algus.lib.lets',
    'lino_algus.lib.users',
    'lino_algus.lib.users.fixtures',
    'lino_algus.projects',
    'lino_algus.projects.algus',
    'lino_algus.projects.algus.tests',
    'lino_algus.projects.algus.settings',
    'lino_algus.projects.algus.settings.fixtures',
])

SETUP_INFO.update(message_extractors={
    'lino_algus': [
        ('**/cache/**', 'ignore', None),
        ('**.py', 'python', None),
        ('**.js', 'javascript', None),
        ('**/config/**.html', 'jinja2', None),
    ],
})

SETUP_INFO.update(package_data=dict())


def add_package_data(package, *patterns):
    l = SETUP_INFO['package_data'].setdefault(package, [])
    l.extend(patterns)
    return l

l = add_package_data('lino_algus.lib.algus')
for lng in 'de fr'.split():
    l.append('locale/%s/LC_MESSAGES/*.mo' % lng)
