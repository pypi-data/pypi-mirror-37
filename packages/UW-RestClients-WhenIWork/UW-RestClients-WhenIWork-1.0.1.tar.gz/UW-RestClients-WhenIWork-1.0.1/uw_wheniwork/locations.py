from . import WhenIWork
from .models import Location


class Locations(WhenIWork):
    def get_location(self, location_id):
        """
        Returns location data.

        http://dev.wheniwork.com/#get-existing-location
        """
        url = "/2/locations/%s" % location_id

        return self.location_from_json(self._get_resource(url)["location"])

    def get_locations(self):
        """
        Returns a list of locations.

        http://dev.wheniwork.com/#listing-locations
        """
        url = "/2/locations"

        data = self._get_resource(url)
        locations = []
        for entry in data['locations']:
            locations.append(self.location_from_json(entry))

        return locations

    @staticmethod
    def location_from_json(data):
        location = Location()
        location.location_id = data["id"]
        location.name = data["name"]
        location.address = data["address"]
        return location
