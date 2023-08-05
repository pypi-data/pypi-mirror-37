from unittest import TestCase

from uw_wheniwork.account import Accounts
from uw_wheniwork.util import fdao_wheniwork_override


@fdao_wheniwork_override
class WhenIWorkTestAccounts(TestCase):

    def test_accounts(self):
        wheniwork = Accounts()

        account = wheniwork.get_account()
        self.assertEquals(account.account_id, 11)
        self.assertEquals(account.company, '123 Company')
