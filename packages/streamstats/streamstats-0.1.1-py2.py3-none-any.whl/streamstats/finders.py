# -*- coding: utf-8 -*-
import requests
import streamstats


class WatershedFinder(object):
    """A watershed finder for spatial points."""
    def __init__(self):
        self.baseurl = "".join([streamstats.base_url, "watershed.geojson"])

    def query(self, state, lon, lat):
        """Query a spatial point, finding its watershed.

        Find the polygon representation of the watershed containing
        a spatial point.

        Args:
            state (str): Two character state code for the state
                containing the point, e.g., "CA" for California.
            lon (float): Longitude of point in decimal degrees.
            lat (float): Latitude of point in decimal degrees.

        Returns:
            GeoDataFrame of watershed that contains the query point.
        """
        payload = {
            'rcode': state,
            'xlocation': lon,
            'ylocation': lat,
            'crs': 4326,
            'includeparameters': True,
            'includeflowtypes': False,
            'includefeatures': True,
            'simplify': False
        }
        r = requests.get(self.baseurl, params=payload)
        r.raise_for_status()  # raises errors early
        return r
