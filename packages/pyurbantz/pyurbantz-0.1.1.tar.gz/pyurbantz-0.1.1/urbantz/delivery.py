from datetime import datetime
from urbantz.utils import Coordinates
from urbantz.exceptions import APIError
import requests


class Delivery(object):
    """
    A UrbanTZ delivery with a unique ID.
    """

    def __init__(self, id):
        """
        :param str id: A delivery ID.
        """
        self.id = id
        """
        The delivery ID.

        :type: str
        """

        self.last_updated = None
        """
        Last API update date/time. Is None if data has never been fetched
        from the API.

        :type: datetime or None
        """

        self.position = None
        """
        Coordinates of the delivery truck's position.

        :type: urbantz.utils.Coordinates
        """

        self.destination = None
        """
        Coordinates of the delivery destination.

        :type: urbantz.utils.Coordinates
        """

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.id)

    @property
    def api_url(self):
        """
        URL pointing to the API endpoint to use for the specific delivery.

        :type: str
        """
        return 'https://backend.urbantz.com/public/task/tracking/' + self.id

    def update(self):
        """
        Fetch the latest delivery information from the API.

        :raises requests.exceptions.HTTPError: If the response has an
           HTTP 4xx or 5xx code.
        :raises urbantz.exceptions.APIError: If the API returned an error.
        """
        resp = requests.get(self.api_url)
        resp.raise_for_status()
        data = resp.json()

        if 'error' in data:
            raise APIError(data['error'])

        self.position = Coordinates.fromJSON(data['position'])
        self.destination = Coordinates.fromJSON(
            data['location']['location']['geometry'])

        self.last_updated = datetime.now()
