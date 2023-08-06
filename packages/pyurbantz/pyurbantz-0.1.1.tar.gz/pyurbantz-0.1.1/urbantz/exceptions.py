class APIError(Exception):
    """
    An error returned by the UrbanTZ API.
    This does not include HTTP errors.
    """

    def __init__(self, error):
        """
        :param error: Parsed JSON error from the API.
        :type error: dict
        """
        self.message = error.get('message')
        self.code = error.get('code')

    def __repr__(self):
        return "<APIError '{}'>".format(str(self))

    def __str__(self):
        return self.message or 'Unknown error'
