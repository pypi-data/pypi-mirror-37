Bio2BEL PFAM |build|
====================

Installation |pypi_version| |python_versions| |pypi_license|
------------------------------------------------------------
``bio2bel_pfam`` can be installed easily from
`PyPI <https://pypi.python.org/pypi/bio2bel_pfam>`_
with the following code in your favorite terminal:

.. code-block:: sh

    $ python3 -m pip install bio2bel_pfam

or from the latest code on `GitHub <https://github.com/bio2bel/pfam>`_ with:

.. code-block:: sh

    $ python3 -m pip install git+https://github.com/bio2bel/pfam.git

Setup
-----
PFAM can be downloaded and populated from either the
Python REPL or the automatically installed command line utility.

Python REPL
~~~~~~~~~~~
.. code-block:: python

    >>> import bio2bel_pfam
    >>> pfam_manager = bio2bel_pfam.Manager()
    >>> pfam_manager.populate()

Command Line Utility
~~~~~~~~~~~~~~~~~~~~
.. code-block:: sh

    bio2bel_pfam populate


.. |build| image:: https://travis-ci.com/bio2bel/pfam.svg?branch=master
    :target: https://travis-ci.org/bio2bel/pfam
    :alt: Build Status

.. |documentation| image:: http://readthedocs.org/projects/bio2bel-pfam/badge/?version=latest
    :target: http://bio2bel.readthedocs.io/projects/pfam/en/latest/?badge=latest
    :alt: Documentation Status

.. |pypi_version| image:: https://img.shields.io/pypi/v/bio2bel_pfam.svg
    :alt: Current version on PyPI

.. |coverage| image:: https://codecov.io/gh/bio2bel/pfam/coverage.svg?branch=master
    :target: https://codecov.io/gh/bio2bel/pfam?branch=master
    :alt: Coverage Status

.. |python_versions| image:: https://img.shields.io/pypi/pyversions/bio2bel_pfam.svg
    :alt: Stable Supported Python Versions

.. |pypi_license| image:: https://img.shields.io/pypi/l/bio2bel_pfam.svg
    :alt: MIT License
