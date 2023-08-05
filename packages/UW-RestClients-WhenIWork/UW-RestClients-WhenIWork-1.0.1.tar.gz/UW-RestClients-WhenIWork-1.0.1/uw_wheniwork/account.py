from . import WhenIWork
from .models import Account


class Accounts(WhenIWork):
    def get_account(self):
        """
        Get Existing Account

        http://dev.wheniwork.com/#get-existing-account
        """
        url = "/2/account/"
        return self.account_from_json(self._get_resource(url)["account"])

    @staticmethod
    def account_from_json(data):
        account = Account()
        account.account_id = data["id"]
        account.company = data["company"]
        account.master_id = data["master_id"]
        return account
