"""
This is the interface for interacting with When I Work's web services.
"""
import json
import re

from restclients_core.exceptions import DataFailureException

from .dao import WhenIWork_DAO


class WhenIWork(object):
    """
    The WhenIWork object has methods for getting information
    about workers and shifts within When I Work
    """

    def __init__(self, token=None):
        self._re_wheniwork_id = re.compile(r'^\d+$')
        self.token = token if token \
            else WhenIWork_DAO().get_service_setting('TOKEN', None)

    def valid_wheniwork_id(self, wheniwork_id):
        return self._re_wheniwork_id.match(str(wheniwork_id)) is not None

    def _get_resource(self, url, data_key=None):
        """
        When I Work GET method. Return representation of the requested
        resource.
        """
        headers = {"Accept": "application/json"}
        if self.token:
            headers["W-Token"] = "%s" % self.token
        response = WhenIWork_DAO().getURL(url, headers)

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return json.loads(response.data)

    def _put_resource(self, url, body):
        """
        When I Work PUT method.
        """
        headers = {"Content-Type": "application/json",
                   "Accept": "application/json"}
        if self.token:
            headers["W-Token"] = "%s" % self.token
        response = WhenIWork_DAO().putURL(url, headers, json.dumps(body))

        if not (response.status == 200 or response.status == 201 or
                response.status == 204):
            raise DataFailureException(url, response.status, response.data)

        return json.loads(response.data)

    def _post_resource(self, url, body):
        """
        When I Work POST method.
        """
        headers = {"Content-Type": "application/json",
                   "Accept": "application/json"}
        if self.token:
            headers["W-Token"] = "%s" % self.token
        response = WhenIWork_DAO().postURL(url, headers, json.dumps(body))

        if not (response.status == 200 or response.status == 204):
            raise DataFailureException(url, response.status, response.data)

        return json.loads(response.data)

    def _delete_resource(self, url):
        """
        When I Work DELETE method.
        """
        headers = {"Content-Type": "application/json",
                   "Accept": "application/json"}
        if self.token:
            headers["W-Token"] = "%s" % self.token
        response = WhenIWork_DAO().deleteURL(url, headers)

        if not (response.status == 200 or response.status == 201 or
                response.status == 204):
            raise DataFailureException(url, response.status, response.data)

        return json.loads(response.data)
