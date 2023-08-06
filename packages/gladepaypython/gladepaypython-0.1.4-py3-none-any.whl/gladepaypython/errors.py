class GladepayError(Exception):
    """
    Python Gladepay Error
    """
    pass

class MissingAuthKeyError(GladepayError):
    """
    We can't find the authentication key
    """
    pass


class InvalidMethodError(GladepayError):
    """
    Invalid or unrecoginised/unimplemented HTTP request method
    """
    pass


class InvalidDataError(GladepayError):
    """
    Invalid input recognised. Saves unecessary trip to server
    """
    pass