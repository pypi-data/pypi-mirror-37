from six.moves.urllib.parse import urlencode

from . import WhenIWork
from .models import User


class Users(WhenIWork):
    def get_user(self, user_id):
        """
        Returns user profile data.

        http://dev.wheniwork.com/#get-existing-user
        """
        url = "/2/users/%s" % user_id

        return self.user_from_json(self._get_resource(url)["user"])

    def get_users(self, params={}):
        """
        Returns a list of users.

        http://dev.wheniwork.com/#listing-users
        """
        param_list = [(k, params[k]) for k in sorted(params)]
        url = "/2/users/?%s" % urlencode(param_list)

        data = self._get_resource(url)
        users = []
        for entry in data["users"]:
            users.append(self.user_from_json(entry))

        return users

    @staticmethod
    def user_from_json(data):
        user = User()
        user.user_id = data["id"]
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.email = data["email"] if "email" in data else None
        user.employee_code = data["employee_code"]

        return user
