Hacking on :mod:`zope.location`
===============================


Getting the Code
################

The main repository for :mod:`zope.location` is in the Zope Foundation
Github repository:

  https://github.com/zopefoundation/zope.location

You can get a read-only checkout from there:

.. code-block:: sh

   $ git clone https://github.com/zopefoundation/zope.location.git

or fork it and get a writeable checkout of your fork:

.. code-block:: sh

   $ git clone git@github.com/jrandom/zope.location.git

The project also mirrors the trunk from the Github repository as a
Bazaar branch on Launchpad:

https://code.launchpad.net/zope.location

You can branch the trunk from there using Bazaar:

.. code-block:: sh

   $ bzr branch lp:zope.location


Working in a ``virtualenv``
###########################

Installing
----------

If you use the ``virtualenv`` package to create lightweight Python
development environments, you can run the tests using nothing more
than the ``python`` binary in a virtualenv.  First, create a scratch
environment:

.. code-block:: sh

   $ /path/to/virtualenv --no-site-packages /tmp/hack-zope.location

Next, get this package registered as a "development egg" in the
environment:

.. code-block:: sh

   $ /tmp/hack-zope.location/bin/python setup.py develop

Running the tests
-----------------

Then, you canrun the tests using the build-in ``setuptools`` testrunner:

.. code-block:: sh

   $ /tmp/hack-zope.location/bin/python setup.py test -q
   ...............................................................................
   ----------------------------------------------------------------------
   Ran 83 tests in 0.037s
   
   OK

If you have the :mod:`nose` package installed in the virtualenv, you can
use its testrunner too:

.. code-block:: sh

   $ /tmp/hack-zope.location/bin/nosetests
   .......................................................................................
   ----------------------------------------------------------------------
   Ran 87 tests in 0.037s
   
   OK

If you have the :mod:`coverage` pacakge installed in the virtualenv,
you can see how well the tests cover the code:

.. code-block:: sh

   $ /tmp/hack-zope.location/bin/easy_install nose coverage
   ...
   $ /tmp/hack-zope.location/bin/nosetests --with coverage
   .......................................................................................
   Name                       Stmts   Miss  Cover   Missing
   --------------------------------------------------------
   zope.location                  5      0   100%   
   zope.location._compat          2      0   100%   
   zope.location.interfaces      23      0   100%   
   zope.location.location        61      0   100%   
   zope.location.pickling        14      0   100%   
   zope.location.traversing      80      0   100%   
   --------------------------------------------------------
   TOTAL                        185      0   100%   
   ----------------------------------------------------------------------
   Ran 87 tests in 0.315s

   OK


Building the documentation
--------------------------

:mod:`zope.location` uses the nifty :mod:`Sphinx` documentation system
for building its docs.  Using the same virtualenv you set up to run the
tests, you can build the docs:

.. code-block:: sh

   $ /tmp/hack-zope.location/bin/easy_install \
    Sphinx repoze.sphinx.autoitnerface zope.component
   ...
   $ cd docs
   $ PATH=/tmp/hack-zope.location/bin:$PATH make html
   sphinx-build -b html -d _build/doctrees   . _build/html
   ...
   build succeeded.

   Build finished. The HTML pages are in _build/html.

You can also test the code snippets in the documentation:

.. code-block:: sh

   $ PATH=/tmp/hack-zope.location/bin:$PATH make doctest
   sphinx-build -b doctest -d _build/doctrees   . _build/doctest
   ...
   running tests...

   ...

   Doctest summary
   ===============
     187 tests
       0 failures in tests
       0 failures in setup code
       0 failures in cleanup code
   build succeeded.
   Testing of doctests in the sources finished, look at the  results in _build/doctest/output.txt.
   


Using :mod:`zc.buildout`
########################

Setting up the buildout
-----------------------

:mod:`zope.location` ships with its own :file:`buildout.cfg` file and
:file:`bootstrap.py` for setting up a development buildout:

.. code-block:: sh

   $ /path/to/python2.7 bootstrap.py
   ...
   Generated script '.../bin/buildout'
   $ bin/buildout
   Develop: '/home/jrandom/projects/Zope/zope.location/.'
   ...
   Got coverage 3.7.1

Running the tests
-----------------

You can now run the tests:

.. code-block:: sh

   $ bin/test --all
   Running zope.testing.testrunner.layer.UnitTests tests:
     Set up zope.testing.testrunner.layer.UnitTests in 0.000 seconds.
     Ran 79 tests with 0 failures and 0 errors in 0.000 seconds.
   Tearing down left over layers:
     Tear down zope.testing.testrunner.layer.UnitTests in 0.000 seconds.



Using :mod:`tox`
################

Running Tests on Multiple Python Versions
-----------------------------------------

`tox <http://tox.testrun.org/latest/>`_ is a Python-based test automation
tool designed to run tests against multiple Python versions.  It creates
a ``virtualenv`` for each configured version, installs the current package
and configured dependencies into each ``virtualenv``, and then runs the
configured commands.
   
:mod:`zope.location` configures the following :mod:`tox` environments via
its ``tox.ini`` file:

- The ``py26``, ``py27``, ``py33``, ``py34``, and ``pypy`` environments
  builds a ``virtualenv`` with ``pypy``,
  installs :mod:`zope.location` and dependencies, and runs the tests
  via ``python setup.py test -q``.

- The ``coverage`` environment builds a ``virtualenv`` with ``python2.6``,
  installs :mod:`zope.location`, installs
  :mod:`nose` and :mod:`coverage`, and runs ``nosetests`` with statement
  coverage.

- The ``docs`` environment builds a virtualenv with ``python2.6``, installs
  :mod:`zope.location`, installs ``Sphinx`` and
  dependencies, and then builds the docs and exercises the doctest snippets.

This example requires that you have a working ``python2.6`` on your path,
as well as installing ``tox``:

.. code-block:: sh

   $ tox -e py26
   GLOB sdist-make: /home/jrandom/projects/Zope/Z3/zope.location/setup.py
   py26 create: /home/jrandom/projects/Zope/Z3/zope.location/.tox/py26
   py26 installdeps: zope.configuration, zope.copy, zope.interface, zope.proxy, zope.schema
   py26 inst: /home/jrandom/projects/Zope/Z3/zope.location/.tox/dist/zope.location-4.0.4.dev0.zip
   py26 runtests: PYTHONHASHSEED='3489368878'
   py26 runtests: commands[0] | python setup.py test -q
   running test
   ...
   ...................................................................................
   ----------------------------------------------------------------------
   Ran 83 tests in 0.066s

   OK
   ___________________________________ summary ____________________________________
     py26: commands succeeded
     congratulations :)
   

Running ``tox`` with no arguments runs all the configured environments,
including building the docs and testing their snippets:

.. code-block:: sh

   $ tox
   GLOB sdist-make: .../zope.location/setup.py
   py26 sdist-reinst: .../zope.location/.tox/dist/zope.location-4.0.2dev.zip
   ...
   Doctest summary
   ===============
     187 tests
       0 failures in tests
       0 failures in setup code
       0 failures in cleanup code
   build succeeded.
   ___________________________________ summary ____________________________________
     py26: commands succeeded
     py27: commands succeeded
     py32: commands succeeded
     py33: commands succeeded
     py34: commands succeeded
     pypy: commands succeeded
     coverage: commands succeeded
     docs: commands succeeded
     congratulations :)


Contributing to :mod:`zope.location`
####################################

Submitting a Bug Report
-----------------------

:mod:`zope.location` tracks its bugs on Github:

  https://github.com/zopefoundation/zope.location/issues

Please submit bug reports and feature requests there.


Sharing Your Changes
--------------------

.. note::

   Please ensure that all tests are passing before you submit your code.
   If possible, your submission should include new tests for new features
   or bug fixes, although it is possible that you may have tested your
   new code by updating existing tests.

If have made a change you would like to share, the best route is to fork
the Githb repository, check out your fork, make your changes on a branch
in your fork, and push it.  You can then submit a pull request from your
branch:

  https://github.com/zopefoundation/zope.location/pulls

If you branched the code from Launchpad using Bazaar, you have another
option:  you can "push" your branch to Launchpad:

.. code-block:: sh

   $ bzr push lp:~jrandom/zope.location/cool_feature

After pushing your branch, you can link it to a bug report on Github,
or request that the maintainers merge your branch using the Launchpad
"merge request" feature.
