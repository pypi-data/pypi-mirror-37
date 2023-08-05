from os.path import abspath, dirname, join

from restclients_core.dao import DAO


class WhenIWork_DAO(DAO):
    def service_name(self):
        return 'wheniwork'

    def service_mock_paths(self):
        return [abspath(join(dirname(__file__), "resources"))]

    def get_default_service_setting(self, key):
        if "HOST" == key:
            return 'https://api.wheniwork.com'
