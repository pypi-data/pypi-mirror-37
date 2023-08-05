Topos Theme
===========

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - pypi
      - |version| |supported-versions|

.. |travis| image:: https://travis-ci.org/alcarney/topos.svg?branch=dev
    :target: https://travis-ci.org/alcarney/topos

.. |coveralls| image:: https://coveralls.io/repos/github/alcarney/topos/badge.svg?branch=dev
    :target: https://coveralls.io/github/alcarney/topos?branch=dev

.. |docs| image:: https://readthedocs.org/projects/topos-theme/badge/?version=latest
    :target: https://topos-theme.readthedocs.io/en/latest/
    :alt: Documentation Status

.. |version| image:: https://img.shields.io/pypi/v/topos-theme.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/topos-theme

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/topos-theme.svg
    :alt: Supported versions
    :target: https://pypi.org/project/topos-theme

:code:`topos-theme` is a HTML theme for `sphinx`_ that was originally developed
for the `topos <topos-gh>`_ python package but it has now been extracted out
into its own independent project.

Getting Started
---------------

To use this theme for your own sphinx sites first you need to install the
:code:`topos-theme` package

.. code-block:: sh

   $ pip install topos-theme

then in your :code:`conf.py`

.. code-block:: python

   extensions = [
       ...,
       "topos_theme"
   ]

   html_theme = "topos-theme"

Finally rebuild your project and you should see that :code:`topos-theme` has taken
effect.


Supported Features
------------------

Because I'm a manic this theme is developed mostly from scratch as such not all
features supported by Sphinx are supported by this theme yet. So here is a list
keeping track of what has and has not been implemented:

- [X] Math rendering via MathJax
- [ ] Searching the Documentation
- [ ] Responsive design

Projects Using this Theme
-------------------------

Here are some projects that are using this theme.

- `stylo`_
- `topos <https://topos.readthedocs.io/en/latest/>`_
- `topos-theme`_

Do you have a project that is making use of this theme? You are more than
welcome to open a pull request to add your project to this list.

.. _sphinx: http://www.sphinx-doc.org/en/master
.. _topos-gh: https://github.com/alcarney/topos
.. _topos-theme: https://topos-theme.readthedocs.io/en/latest/
.. _stylo: https://alcarney.github.io/stylo/
