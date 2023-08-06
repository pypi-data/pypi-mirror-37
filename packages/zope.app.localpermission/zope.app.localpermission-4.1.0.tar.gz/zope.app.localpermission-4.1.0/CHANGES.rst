=========
 CHANGES
=========

4.1.0 (2018-10-19)
==================

- Add support for Python 3.7.


4.0.0 (2017-04-23)
==================

- Add support for PyPy.
- Add support for Python 3.4, 3.5, and 3.6.
- Remove dependency on ZODB3. Instead, depend on the separate
  ``persistent`` package.


3.7.2 (2010-03-21)
==================

- Added missing i18n domain to ``browser.zcml``.

3.7.1 (2010-02-22)
==================

- The zope.app namespace wasn't declared correctly.

3.7.0 (2009-03-14)
==================

Initial release. This package was extracted from zope.app.security to separate
the functionality without additional dependencies.
