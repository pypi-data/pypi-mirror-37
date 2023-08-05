from unittest import TestCase

from uw_wheniwork.sites import Sites
from uw_wheniwork.util import fdao_wheniwork_override


@fdao_wheniwork_override
class WhenIWorkTestSites(TestCase):

    def test_sites(self):
        wheniwork = Sites()

        site = wheniwork.get_site(9)
        self.assertEquals(site.address, '1600 S Azusa Ave, '
                                        'City of Industry, CA 91748')

        site = wheniwork.create_site({
            'name': 'Shaded Grove',
        })
        self.assertEquals(site.name, 'Shaded Grove')
