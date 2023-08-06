********************************************
Recipe for compiling and installing software
********************************************

.. contents::

The recipe provides the means to compile and install source distributions
using ``configure`` and ``make`` and other similar tools. It is inspired by
the hexagonit.recipe.cmmi_ recipe but provides more control over the build process.

Use python 2.7 to run test, at least python 2.6 results in some
failures in the tests.py:

  TypeError: failUnlessRaises() takes at least 3 arguments (2 given)

First, we make test environments:

::

  cd slapos.recipe.cmmi
  wget http://downloads.buildout.org/2/bootstrap.py
  wget http://svn.zope.org/*checkout*/zc.buildout/trunk/bootstrap/bootstrap.py

  cat <<EOF > buildout.cfg
  [buildout]
  develop = .
  parts = test
  prefix = /tmp/test

  [test]
  recipe = zc.recipe.testrunner
  eggs =
    slapos.recipe.cmmi[test]
  EOF

  python -S bootstrap.py --version 1.7.0
  bin/buildout

It will generate script bin/test, run it to do all the testcases:

::

  bin/test

After source changed, run buildout to update eggs again:

::

  bin/buildout -v -N
  bin/test

Build dist/slapos.recipe.cmmi-0.2-py2.7.egg

::

  bin/buildout setup setup.py bdist_egg

Build source package dist/slapos.recipe.cmmi-0.2.tar.gz

::

  python setup.py sdist

Repository: http://git.erp5.org/gitweb/slapos.recipe.cmmi.git

Clone URL: git clone http://git.erp5.org/repos/slapos.recipe.cmmi.git

Issue tracker: None

Supported Python versions: 2.6, 2.7, 3.2, 3.3

Supported zc.buildout versions: 1.x, 2.x

Travis build: |travis|

.. |travis| image:: https://api.travis-ci.org/hexagonit/hexagonit.recipe.cmmi.png

.. _hexagonit.recipe.cmmi : http://pypi.python.org/pypi/hexagonit.recipe.cmmi
