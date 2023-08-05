from unittest import TestCase

from uw_wheniwork.shifts import Shifts
from uw_wheniwork.util import fdao_wheniwork_override


@fdao_wheniwork_override
class WhenIWorkTestShifts(TestCase):

    def test_shifts(self):
        wheniwork = Shifts()

        shifts = wheniwork.get_shifts({
            'location_id': 1,
            'start': '2014-03-05 00:00:00',
            'end': '2014-03-08 23:59:59',
        })
        self.assertEquals(shifts[0].shift_id, 10000)
        self.assertEquals(shifts[1].site_id, 4351)
        self.assertEquals(shifts[1].notes, 'We need more cowbell.')

        shift = wheniwork.create_shift({
            'notes': 'Come in early today.',
        })
        self.assertEquals(shift.notes, 'Come in early today.')

        ret = wheniwork.delete_shifts([1337])
        self.assertTrue(ret["success"])
