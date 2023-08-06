# -*- coding: utf-8 -*-


class SchemingError(Exception):
    """Base class for all exceptions in the scheming module.
    """


class SchemingOperationError(SchemingError):
    """Used when a database operation fails.

    :ivar orignal_exc: Contains the original exception raised by the
      underlying DB-API2 module.
    """
    original_exc = None
