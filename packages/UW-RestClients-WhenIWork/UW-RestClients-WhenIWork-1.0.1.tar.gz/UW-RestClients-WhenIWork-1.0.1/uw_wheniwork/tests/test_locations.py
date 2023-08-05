from unittest import TestCase

from uw_wheniwork.locations import Locations
from uw_wheniwork.util import fdao_wheniwork_override


@fdao_wheniwork_override
class WhenIWorkTestLocations(TestCase):

    def test_locations(self):
        wheniwork = Locations()

        locations = wheniwork.get_locations()
        self.assertEquals(locations[0].location_id, 136)
        self.assertEquals(locations[1].address, '100 Courthouse Square, '
                                                'Hill Valley, CA 12345')

        location = wheniwork.get_location(136)
        self.assertEquals(location.name, 'Downtown')
