==============================
Memair Google Takeout Importer
==============================

.. image:: https://badge.fury.io/py/gtmem.svg
    :target: https://badge.fury.io/py/gtmem

.. image:: http://img.shields.io/badge/license-MIT-yellow.svg?style=flat
    :target: https://github.com/memair/google-takeout-importer/blob/master/LICENSE

.. image:: https://img.shields.io/badge/contact-Gregology-blue.svg?style=flat
    :target: http://gregology.net/contact/

Overview
--------

A command line tool for importing Goole Takeout data into Memair. Currently the tool only imports Location History but more options will be added shortly.

Installation
------------

``gtmem`` is available on PyPI

http://pypi.python.org/pypi/gtmem

Install via ``pip``
::

    $ pip install gtmem

Or via ``easy_install``
::

    $ easy_install gtmem

Or directly from ``memair``'s `git repo <https://github.com/memair/google-takeout-importer>`__
::

    $ git clone git://github.com/memair/google-takeout-importer.git
    $ cd google-takeout-importer
    $ python setup.py install


Basic usage
-----------

`Generate a temporary access token <https://memair.com/generate_own_access_token>`__

`Download your location history data as JSON from Google Takeout <https://takeout.google.com/settings/takeout>`__

.. image:: https://user-images.githubusercontent.com/1595448/46702260-6a407980-cbf0-11e8-8ae9-3c6a1893484b.png
   :width: 80 %

Extract the zip and run;

::

    $ gtmem -m 0000000000000000000000000000000000000000000000000000000000000000 -g ~/Downloads/Takeout


replacing 00000... with your access_token


Running Test
------------

coming shortly...

Python compatibility
--------------------

Developed for Python 3. May work but not tested in Python 2.
