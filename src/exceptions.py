class ConnectionError(BaseException):
    """
    Returns a string showing the database connection status.
    """
    def __init__(self, exception):
        self.inner_exception = exception

    def __str__(self):
        return str(self.inner_exception)

class FileNotFoundError(BaseException):
    """
    Returns an exception string when a file cannot be found at the intended path.
    """
    def __init__(self, exception):
        self.inner_exception = exception
    
    def __str__(self):
        return str(self.inner_exception)