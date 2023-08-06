.. contents:: Table of Contents


Introduction
============


This package is an addon for `ftw.simplelayout <http://github.com/4teamwork/ftw.simplelayout>`_. Please make sure you
already installed ``ftw.simplelayout`` on your plone site before installing this addon.

FaqBlock provides the integration of an FAQ styled collapsible block on a page
powered by ftw.simplelayout. It uses the existing functionality of ``ftw.simplelayout.TextBlock``.

Compatibility
-------------

Plone 4.3.x


Installation
============

- Add the package to your buildout configuration:

::

    [instance]
    eggs +=
        ...
        ftw.faqblock


Development
===========

1. Fork this repo
2. Clone your fork
3. Shell: ``ln -s development.cfg buildout.cfg``
4. Shell: ``python bootstrap.py``
5. Shell: ``bin/buildout``

Run ``bin/test`` to test your changes.

Or start an instance by running ``bin/instance fg``.


Links
=====

- Github: https://github.com/4teamwork/ftw.faqblock
- Issues: https://github.com/4teamwork/ftw.faqblock/issues
- Pypi: http://pypi.python.org/pypi/ftw.faqblock


Copyright
=========

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.faqblock`` is licensed under GNU General Public License, version 2.
