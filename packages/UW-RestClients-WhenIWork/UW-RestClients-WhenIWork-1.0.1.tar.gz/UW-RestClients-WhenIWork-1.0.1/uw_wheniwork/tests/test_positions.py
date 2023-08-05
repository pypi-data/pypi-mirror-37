from unittest import TestCase

from uw_wheniwork.positions import Positions
from uw_wheniwork.util import fdao_wheniwork_override


@fdao_wheniwork_override
class WhenIWorkTestPositions(TestCase):

    def test_positions(self):
        wheniwork = Positions()

        positions = wheniwork.get_positions()
        self.assertEquals(positions[0].name, 'Stocker')
        self.assertEquals(positions[1].name, 'Bagger')
        self.assertEquals(positions[2].name, 'Cashier')

        position = wheniwork.get_position(32)
        self.assertEquals(position.name, 'Stocker')
