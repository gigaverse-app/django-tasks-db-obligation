"""
django-tasks-db's worker, checked by a pytest-obligation contract.

These are pytest tests (``pytest tests/obligation``), on PostgreSQL and Python 3.11
or later. Django's own test runner (``manage.py test``) skips this package.
"""

import unittest


def load_tests(
    loader: unittest.TestLoader, standard_tests: unittest.TestSuite, pattern: str | None
) -> unittest.TestSuite:
    return unittest.TestSuite()
