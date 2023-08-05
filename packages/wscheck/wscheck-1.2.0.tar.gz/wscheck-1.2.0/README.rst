WSCheck
=======

|PyPi| |Build| |Docs| |DependencyStatus| |CodeQuality| |Coverage| |License|

`WSCheck <https://github.com/andras-tim/wscheck>`__ is a static analysis tool for whitespaces.


Installation
------------

.. code-block:: bash

    $ pip install wscheck


Usage
-----

**Check multiple files:**

.. code-block:: bash

    $ wscheck orange.sh pineapple.xml kiwi.js

**Exclude rules:**

.. code-block:: bash

    $ wscheck --exclude WSC002 --exclude WSC003 orange.sh

**Get list of available rules:**

.. code-block:: bash

    $ wscheck --list-rules

For details about rules, see `Rules <http://wscheck.readthedocs.io/en/latest/rules/index.html>`__

**Write CheckStyle output too:**

.. code-block:: bash

    $ wscheck --checkstyle results.xml pineapple.xml


Example
-------

.. code-block:: bash

    $ wscheck examples/multiple_problems.py

.. code-block:: none

    In examples/multiple_problems.py line 2:
    class LabelPrinter:
    ^-- WSC007: File begins with newline

    In examples/multiple_problems.py line 6:
            self.print_to_pdf()
                               ^-- WSC002: Tailing whitespace

    In examples/multiple_problems.py line 9:
       def __generate_pdf(self):
       ^-- WSC003: Indentation is not multiple of 2

    In examples/multiple_problems.py line 10:
            pdf_generator = _LabelPdfGenerator()
                                                ^-- WSC001: Bad line ending '\r\n'

    In examples/multiple_problems.py line 16:
    --->--->os.makedirs(self.__cache_dir, exist_ok=True)
    ^-- WSC004: Indentation with non-space character

    In examples/multiple_problems.py line 22:
            return os.path.join(self.__cache_dir, pdf_name)
                                                           ^-- WSC006: Too many newline at end of file (+1)


Bugs
----

Bugs or suggestions? Visit the `issue tracker <https://github.com/andras-tim/wscheck/issues>`__.


Benchmark
---------

* You can run a quick benchmark:

    .. code-block:: bash

        tox -- tests/performance --quick-benchmark

* You can run benchmarks and generate histogram for compare calls to each other:

    .. code-block:: bash

        tox -- tests/performance --benchmark-histogram

* You can run benchmarks and save results for later compare:

    .. code-block:: bash

        tox -- tests/performance --benchmark-save=foo

* You can run benchmarks and compare with the last saved result with fail treshold:

    .. code-block:: bash

        tox -- tests/performance --benchmark-histogram --benchmark-compare --benchmark-compare-fail=mean:5% --benchmark-sort=name

* You can run benchmarks and compare with the last saved result by groups:

    .. code-block:: bash

        tox -- tests/performance --benchmark-histogram --benchmark-compare --benchmark-group-by=func

        tox -- tests/performance --benchmark-histogram --benchmark-compare --benchmark-group-by=name


.. |Build| image:: https://travis-ci.org/andras-tim/wscheck.svg?branch=master
    :target: https://travis-ci.org/andras-tim/wscheck/branches
    :alt: Build Status
.. |DependencyStatus| image:: https://requires.io/github/andras-tim/wscheck/requirements.svg?branch=master
    :target: https://requires.io/github/andras-tim/wscheck/requirements/?branch=master
    :alt: Dependency Status
.. |PyPi| image:: https://img.shields.io/badge/download-PyPi-green.svg
    :target: https://pypi.org/project/wscheck/
    :alt: Python Package
.. |Docs| image:: https://readthedocs.org/projects/wscheck/badge/?version=latest
    :target: http://wscheck.readthedocs.org/en/latest/
    :alt: Documentation Status
.. |License| image:: https://img.shields.io/badge/license-GPL%203.0-blue.svg
    :target: https://github.com/andras-tim/wscheck/blob/master/LICENSE
    :alt: License

.. |CodeQuality| image:: https://api.codacy.com/project/badge/Grade/448b73826c97497d8bf0e2970cba1156
    :target: https://www.codacy.com/app/andras-tim/wscheck
    :alt: Code Quality
.. |Coverage| image:: https://coveralls.io/repos/andras-tim/wscheck/badge.svg?branch=master&service=github
    :target: https://coveralls.io/r/andras-tim/wscheck?branch=master&service=github
    :alt: Test Coverage

.. |IssueStats| image:: https://img.shields.io/github/issues/andras-tim/wscheck.svg
    :target: http://issuestats.com/github/andras-tim/wscheck
    :alt: Issue Stats
