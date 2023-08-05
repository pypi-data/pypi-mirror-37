================
 Dungeon Sheets
================

A tool to create character sheets for Dungeons and Dragons.

.. image:: https://travis-ci.com/canismarko/dungeon-sheets.svg?branch=master
    :target: https://travis-ci.com/canismarko/dungeon-sheets

Installation
============

.. code:: bash

    $ pip install dungeonsheets

.. note::

   Dungeon sheets requires **at least python 3.6**. This is mostly due
   to the liberal use of f-strings_. If you want to use it with
   previous versions of python 3, you'll probably have to replace all
   the f-strings with the older ``.format()`` method or string
   interpolation.

.. _f-strings: https://www.python.org/dev/peps/pep-0498/

External dependencies
=====================

* You will need **pdftk** installed to generate the sheets in PDF format.
* You will need **pdflatex** installed to generate the PDF spell pages (optional).

.. note::

   Different linux distributions have different names for packages. While
   pdftk is available in Debian and derivatives as **pdftk**, the package
   is not available in some RPM distributions, such as Fedora and CentOS.
   One alternative would be to build your PC sheets using docker.

.. note::

   If the ``pdflatex`` command is available on your system,
   spellcasters will include a spellbook with descriptions of each
   spell known. If not, then this feature will be skipped.

Usage
=====

Each character is described by a python file, which gives many
attributes associated with the character. See examples_ for more
information about the character descriptions.

.. _examples: https://github.com/canismarko/dungeon-sheets/tree/master/examples

The PDF's can then be generated using the ``makesheets`` command.

.. code:: bash

    $ cd examples
    $ makesheets wizard.py

dungeon-sheets contains definitions for standard weapons and spells,
so attack bonuses and damage can be calculated automatically.

If you'd like a **step-by-step walkthrough** for creating a new
character, just run ``create-character`` from a command line and a
helpful menu system will take care of the basics for you.
