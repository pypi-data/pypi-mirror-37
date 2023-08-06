.. epigraph:: al·pha·bet soup
              /ˈalfəˌbet so͞op/Submit
              noun INFORMAL
              incomprehensible or confusing language, typically containing many abbreviations or symbols.


alphabetsoup fixes problems with protein FASTA files:
+--------------------------+------------------------+
| Problem                  | Fix                    |
+--------------------------+------------------------+
| Unknown character        | Replaces with 'X'      |
+--------------------------+------------------------+
| Stop/ambigous at ends    | Trims                  |
+--------------------------+------------------------+
| Stop/ambiguous in middle | Optionally fragments   |
+--------------------------+------------------------+
| Too short                | Deletes record         |
+--------------------------+------------------------+


+-------------------+------------+------------+
| Latest Release    | |pypi|     | |Soup|     |
+-------------------+------------+            +
| GitHub            | |repo|     |            |
+-------------------+------------+            +
| License           | |license|  |            |
+-------------------+------------+            +
| Documentation     | |rtd|      |            |
+-------------------+------------+            +
| Travis Build      | |travis|   |            |
+-------------------+------------+            +
| Coverage          | |coverage| |            |
+-------------------+------------+            +
| Pythonicity       | |landscape||            |
+-------------------+------------+            +
| Code Grade        | |codacy|   |            |
+-------------------+------------+            +
| Dependencies      | |pyup|     |            |
+-------------------+------------+            +
| Issues            | |issues|   |            |
+-------------------+------------+            +
| Kanban            | |ZenHub|   |            |
+-------------------+------------+------------+


.. |Soup| image:: docs/alphabetsoup.webp
     :target: https://en.wikipedia.org/wiki/Alphabet_soup_(linguistics)
     :alt: Alphabet Soup Definition

.. |pypi| image:: https://img.shields.io/pypi/v/alphabetsoup.svg
    :target: https://pypi.python.org/pypi/alphabetsoup
    :alt: Python package

.. |repo| image:: https://img.shields.io/github/commits-since/ncgr/alphabetsoup/0.01.svg
    :target: https://github.com/ncgr/alphabetsoup
    :alt: GitHub repository

.. |license| image:: https://img.shields.io/badge/License-BSD%203--Clause-blue.svg
    :target: https://github.com/ncgr/alphabetsoup/blob/master/LICENSE.txt
    :alt: License terms

.. |rtd| image:: https://readthedocs.org/projects/alphabetsoup/badge/?version=latest
    :target: http://alphabetsoup.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Server

.. |travis| image:: https://img.shields.io/travis/ncgr/alphabetsoup.svg
    :target:  https://travis-ci.org/ncgr/alphabetsoup
    :alt: Travis CI

.. |landscape| image:: https://landscape.io/github/ncgr/alphabetsoup/master/landscape.svg?style=flat
    :target: https://landscape.io/github/ncgr/alphabetsoup
    :alt: landscape.io status

.. |codacy| image:: https://api.codacy.com/project/badge/Grade/2ebc65ca90f74dc7a9238c202f327981
    :target: https://www.codacy.com/app/joelb123/alphabetsoup?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=LegumeFederation/lorax&amp;utm_campaign=Badge_Grade
    :alt: Codacy.io grade

.. |coverage| image:: https://codecov.io/gh/ncgr/alphabetsoup/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/ncgr/alphabetsoup
    :alt: Codecov.io test coverage

.. |issues| image:: https://img.shields.io/github/issues/LegumeFederation/lorax.svg
    :target:  https://github.com/ncgr/alphabetsoup/issues
    :alt: Issues reported

.. |requires| image:: https://requires.io/github/ncgr/alphabetsoup/requirements.svg?branch=master
     :target: https://requires.io/github/ncgr/alphabetsoup/requirements/?branch=master
     :alt: Requirements Status

.. |pyup| image:: https://pyup.io/repos/github/ncgr/alphabetsoup/shield.svg
     :target: https://pyup.io/repos/github/ncgr/alphabetsoup/
     :alt: pyup.io dependencies

.. |ZenHub| image:: https://raw.githubusercontent.com/ZenHubIO/support/master/zenhub-badge.png
    :target: https://zenhub.com
    :alt: Powered by ZenHub


