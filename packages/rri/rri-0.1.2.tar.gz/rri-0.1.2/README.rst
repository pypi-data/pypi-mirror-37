============================
Registry Reporting Interface
============================

Python client library for the `ICANN Registry Reporting Interface`_.

.. image:: https://img.shields.io/pypi/v/rri.svg
        :target: https://pypi.python.org/pypi/rri

.. image:: https://img.shields.io/travis/storeyio/rri/master.svg
        :target: https://travis-ci.org/storeyio/rri


* Free software: MIT license


Features
--------

rri supports all features of the `ICANN Registry Reporting Interface`_ (v8)

Status checking and submission of:

- Data Escrow Reports

- Data Escrow Notifications

- Registry Functions Activity Report

- Per-Registrar Transactions Report


.. _`ICANN Registry Reporting Interface`: https://tools.ietf.org/html/draft-lozano-icann-registry-interfaces

Installation
============

You can download and install the latest version of this software from the
Python package index (PyPI) as follows::

    pip install --upgrade rri


Usage
=====

.. code-block::

    import rri

    rric = RRIClient('example', 'exampleuser', 'examplepassword')

    if rric.report.check():
        print("We have notified ICANN our .example escrow has been deposited")

Credits
=======

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
