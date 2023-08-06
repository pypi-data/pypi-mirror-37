# -*- coding: utf-8 -*-


class RRIException(Exception):
    pass


class InvalidInput(RRIException):
    """Returned in the case of a HTTP/400 response"""
    pass


class InvalidTldCredentials(RRIException):
    """Returned in the case of a HTTP/401 response"""
    pass


class InvalidAccess(RRIException):
    """Returned in the case of a HTTP/403 response"""
    pass


class InvalidRequestMethod(RRIException):
    """Returned in the case of a HTTP/405 response"""
    pass


class GeneralFailure(RRIException):
    """Returned in the case of a HTTP/500 response"""
    pass


class NotImplemented(RRIException):
    """Returned in the case of a HTTP/501 response"""
    pass


class UnknownStatus(RRIException):
    """Unknown HTTP response"""
    pass
