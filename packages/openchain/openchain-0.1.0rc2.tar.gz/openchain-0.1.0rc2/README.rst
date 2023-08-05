Openchain Library
=================

About
-----

Library for creating blockchain networks.

.. image:: https://circleci.com/bb/manti_by/openchain/tree/master.svg?style=shield&circle-token=7f803605b49718f938b3c300f707ba4fc188cb1e
    :target: https://circleci.com/bb/manti_by/openchain/tree/master

.. image:: https://codecov.io/bb/manti_by/openchain/branch/master/graph/badge.svg
  :target: https://codecov.io/bb/manti_by/openchain

.. image:: https://img.shields.io/badge/license-BSD-blue.svg
    :target: https://bitbucket.org/manti_by/openchain/raw/a482d552071732134966ae28262d1eef5a19b19d/LICENSE.txt

Author: Alexander Chaika <manti.by@gmail.com>

Source link: https://bitbucket.org/manti_by/openchain

Requirements:

- Base - Python 3.5+, ECSDA, LevelDB/Plyvel
- Development - Flake8, Coverage
- Examples - Docker, Tornado

Installation
------------

Install system libraries

    $ sudo apt install python3-dev libleveldb-dev

Install package from `PyPi <https://pypi.org/pypi/openchain>`_

    $ pip install openchain

Alternatively clone from `Bitbucket <https://bitbucket.org/manti_by/openchain>`_

    $ git clone git@bitbucket.org:manti_by/openchain.git

    $ cd openchain/

    $ python setup.py install

Environment variables
---------------------

- $DATABASE_PATH - path to store LevelDB files

Run unit tests and coverage
---------------------------

    $ mkdir -p /var/tmp/leveldb/test/

    $ export DATABASE_PATH='/var/tmp/leveldb/test/'

    $ python -m unittest discover -s openchain/tests/ -p ``'*_tests.py'``

    $ coverage run -m unittest discover -s openchain/tests/ -p ``'*_tests.py'``

    $ coverage xml && coverage report -m


**For more information about how to run examples, please refer to
`README <https://bitbucket.org/manti_by/openchain/src/8013112f6f63022d684350acf5d687aa20d5bd9b/examples/?at=master>`_
in the examples directory**