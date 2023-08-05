Pingstats, a simple CLI based ping visualization script
=======================================================

This script provides a very simple CLI based ping visualization script by utilizing `hipster plot`_.

This project is a much simplified version of PingStats_, a project of mine that went from being useful (i.e, the functionality of this script) to an over complicated mess of spaghetti code. That software provides GUI based plotting, as well as CSV based logging of ping data over time.

INSTALLATION
============

Installation has been made easy on any Unix based system that implements ``pip3``.
::

  pip3 install pingstats

.. note:: For versions previous to V0.4.3, manual install must be used. All versions aside from V0.1 can be installed by cloning the repository and recreating the install script manually.

Usage
=====

This software was implemented with simplicity in mind, and only provides one point of access:
::

  pingstats google.ca

Examples of software in use
===========================

.. image:: http://i64.tinypic.com/33mv6ud.png


In this image, we can see two separate outputs. The top display is a display of the most recent actual return times, whereas the bottom display is the average return time for each sequence.

This display automatically scales to whatever window you have open, adding more lines and columns as necessary.


Running the tests
=================

To run the tests, clone the repository:
::

  git clone https://gitlab.com/eclectickmediasolutions/pingstats.git

Then simply run:
::

  python3 setup.py test


.. _`hipster plot`: https://github.com/imh/hipsterplot
.. _PingStats: https://github.com/eclectickmedia/pingstats
