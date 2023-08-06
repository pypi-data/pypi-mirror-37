class APIError(Exception):

    def __init__(self, error):
        self.message = error.get('message')
        self.code = error.get('code')

    def __repr__(self):
        return "<APIError '{}'>".format(str(self))

    def __str__(self):
        return self.message or 'Unknown error'
