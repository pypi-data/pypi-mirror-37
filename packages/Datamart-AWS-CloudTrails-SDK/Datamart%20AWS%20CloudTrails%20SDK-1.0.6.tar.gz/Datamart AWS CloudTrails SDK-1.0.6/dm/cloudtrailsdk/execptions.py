
class ExceptionTracker(Exception):
    """

    """

    def __init__(self, real_exception):
        """

        :param real_exception:
        """
        self.real_exception = real_exception
