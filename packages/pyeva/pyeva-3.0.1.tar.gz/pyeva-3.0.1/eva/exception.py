"""
Global Web exception and warning classes.
"""


class WebRuntimeWarning(RuntimeWarning):
    pass


class ImproperlyConfigured(Exception):

    """Web is somehow improperly configured"""
    pass


class WebUrlError(Exception):
    pass


class WebDBError(Exception):
    pass


class EvaError(Exception):
    pass
