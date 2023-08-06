====
Aspy
====

|pipeline-badge| |coverage-badge| |docs-badge| |pypi-badge|

aspy is a python library for producing Activity Streams 2.0 content. It doesn‘t
have a lot of features (no extensions) but aims to be give correct results and
be easy to understand.

At the moment, only supports writing activity streams.

Examples
--------

.. code-block:: python

   import aspy

   martin = aspy.Actor(id='http://www.test.example/martin')
   activity = aspy.Create(
       actor=martin,
       summary='Martin created an image',
       object='http://example.org/foo.jpg',
   )
   # do this to serialize it
   json_string = str(activity)



Caveats
-------

We completely don't support extension types at the moment.

Alternatives
------------

The only python Activity Streams 2 library I know of is `activipy
<https://pypi.org/project/activipy/>`_. It supports extension types, but it‘s
still pre-alpha and seems to have been forgotten.


.. |pipeline-badge| image:: https://gitlab.com/alantrick/aspy/badges/master/pipeline.svg
   :target: https://gitlab.com/alantrick/aspy/
   :alt: Build Status

.. |coverage-badge| image:: https://gitlab.com/alantrick/aspy/badges/master/coverage.svg
   :target: https://gitlab.com/alantrick/aspy/
   :alt: Coverage Status

.. |docs-badge| image:: https://img.shields.io/readthedocs/aspy.svg
   :target: `the documentation`_
   :alt: Documentation

.. |pypi-badge| image:: https://img.shields.io/pypi/v/aspy.svg
   :target: https://pypi.org/project/aspy/
   :alt: Project on PyPI

.. _the documentation: http://aspy.readthedocs.io/en/latest/?badge=latest



