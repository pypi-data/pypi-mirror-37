==========================
The ``lino-algus`` package
==========================





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


