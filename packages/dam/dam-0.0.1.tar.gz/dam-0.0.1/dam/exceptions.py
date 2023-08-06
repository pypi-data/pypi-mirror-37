class DAMException(Exception):
    """ Base exception. """

class BadCredentials(DAMException):
    """ Given credentials are not valid. """

class NoInput(DAMException):
    """ Called a method with only optional args without passing any optional args """
