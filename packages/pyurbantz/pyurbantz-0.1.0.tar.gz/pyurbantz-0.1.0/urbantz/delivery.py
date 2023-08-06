from datetime import datetime
from urbantz.utils import Coordinates
from urbantz.exceptions import APIError
import requests


class Delivery(object):
    """
    A UrbanTZ delivery with a unique ID.
    """

    def __init__(self, id):
        self.id = id
        self.last_updated = None
        self.position = None
        self.destination = None

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.id)

    @property
    def api_url(self):
        return 'https://backend.urbantz.com/public/task/tracking/' + self.id

    def update(self):
        resp = requests.get(self.api_url)
        resp.raise_for_status()
        data = resp.json()

        if 'error' in data:
            raise APIError(data['error'])

        self.position = Coordinates.fromJSON(data['position'])
        self.destination = Coordinates.fromJSON(
            data['location']['location']['geometry'])

        self.last_updated = datetime.now()
