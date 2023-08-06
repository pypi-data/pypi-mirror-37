from atelier.invlib import setup_from_tasks
ns = setup_from_tasks(
    globals(), "lino_algus",
    languages="en de fr".split(),
    # tolerate_sphinx_warnings=True,
    locale_dir='lino_algus/lib/algus/locale',
    revision_control_system='git',
    cleanable_files=['docs/api/lino_algus.*'],
    demo_projects=['lino_algus/projects/algus'])


