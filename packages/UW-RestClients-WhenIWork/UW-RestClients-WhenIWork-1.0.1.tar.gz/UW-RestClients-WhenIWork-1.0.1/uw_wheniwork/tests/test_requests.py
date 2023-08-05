from unittest import TestCase

from uw_wheniwork.requests import Requests
from uw_wheniwork.util import fdao_wheniwork_override


@fdao_wheniwork_override
class WhenIWorkTestRequests(TestCase):

    def test_requests(self):
        wheniwork = Requests()

        requests = wheniwork.get_requests({'start': '2012-03-01',
                                           'end': '2012-04-30'})
        self.assertEquals(requests[0].user_id, 135)
        self.assertEquals(requests[1].user_id, 135)

    def test_paged_requests(self):
        wheniwork = Requests()

        requests = wheniwork.get_requests({'start': '2012-05-01',
                                           'end': '2012-05-30'})
        self.assertEqual(len(requests), 6)
