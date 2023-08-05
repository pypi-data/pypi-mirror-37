Dynamo Consistency
==================

|build-status|

Dynamo Consistency is the consistency plugin for Dynamo Dynamic Data Management System.
It provides some standalone executables to run the check as well as
manipulate the sites' running and reporting statuses.

The package also includes a number of modules that can be imported independently
to create custom consistency checks.
A simple consistency check on a site can be done by doing the following
when an instance of ``dynamo`` is installed::

  from dynamo_consistency import config, datatypes, remotelister, inventorylister

  config.LOCATION = '/path/to/config.json'
  site = 'T2_US_MIT'     # For example

  inventory_listing = inventorylister.listing(site)
  remote_listing = remotelister.listing(site)

  datatypes.compare(inventory_listing, remote_listing, 'results')

In this example,
the list of file LFNs in the inventory and not at the site will be in ``results_missing.txt``.
The list of file LFNs at the site and not in the inventory will be in ``results_orphan.txt``.
The ``listing`` functions can be reimplemented to preform the check desired.

Installation
++++++++++++

Dynamo Consistency requires modules ``htcondor`` and ``XRootD`` to be installed separately.
In addition, it uses the Dynamo Dynamic Data Management package to get inventory listings
and to report results of the consistency check.
Any other needed packages are installed with Dynamo Consistency during installation.

The simplest way to install is through pip::

  pip install dynamo-consistency

The source code is maintained on `GitHub <https://github.com/SmartDataProjects/dynamo-consistency>`_.
Other typical ``setuptools`` methods are supported by the repository's ``setup.py``.

.. |build-status| image:: https://travis-ci.org/SmartDataProjects/dynamo-consistency.svg?branch=master
   :target: https://travis-ci.org/SmartDataProjects/dynamo-consistency
