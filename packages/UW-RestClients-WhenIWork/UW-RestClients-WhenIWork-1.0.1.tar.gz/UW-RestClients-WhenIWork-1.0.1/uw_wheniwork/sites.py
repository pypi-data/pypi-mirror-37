from . import WhenIWork
from .models import Site


class Sites(WhenIWork):
    def get_site(self, site_id):
        """
        Returns site data.

        http://dev.wheniwork.com/#get-existing-site
        """
        url = "/2/sites/%s" % site_id

        return self.site_from_json(self._get_resource(url)["site"])

    def get_sites(self):
        """
        Returns a list of sites.

        http://dev.wheniwork.com/#listing-sites
        """
        url = "/2/sites"

        data = self._get_resource(url)
        sites = []
        for entry in data['sites']:
            sites.append(self.site_from_json(entry))

        return sites

    def create_site(self, params={}):
        """
        Creates a site

        http://dev.wheniwork.com/#create-update-site
        """
        url = "/2/sites/"
        body = params

        data = self._post_resource(url, body)
        return self.site_from_json(data["site"])

    @staticmethod
    def site_from_json(data):
        site = Site()
        site.site_id = data["id"]
        site.name = data["name"]
        if data["location_id"]:
            site.location_id = data["location_id"]
        site.address = data["address"]
        return site
