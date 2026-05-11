import psycopg2
from psqlConfig import database, user, password
import requests
import math


class DataSource:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=database,
            user=user,
            password=password,
            host="localhost"
        )

    def getTopSpeciesNear(self, lat, lon, radius_miles=10, top_n=3):
        """
        Returns the top n most observed species per taxon within a bounding box
        approximation of the given radius around (lat, lon).
        """
        lat_delta = radius_miles / 69.0
        lon_delta = radius_miles / (69.0 * math.cos(math.radians(lat)))

        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT iconic_taxon, taxon_name, common_name, COUNT(*) AS count
            FROM observations
            WHERE latitude  BETWEEN %s AND %s
              AND longitude BETWEEN %s AND %s
            GROUP BY iconic_taxon, taxon_name, common_name
            ORDER BY iconic_taxon, count DESC
        """, (lat - lat_delta, lat + lat_delta, lon - lon_delta, lon + lon_delta))

        results = []
        counts = {}
        for row in cursor.fetchall():
            taxon = row[0]
            counts[taxon] = counts.get(taxon, 0) + 1
            if counts[taxon] <= top_n:
                results.append(row)
        return results

    def getLeaderboard(self, common_name_of_animal, top_n=100):
        """Returns top contributors for a given species."""
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT observer, COUNT(*) AS count
            FROM observations
            WHERE common_name = %s
            GROUP BY observer
            ORDER BY count DESC
            LIMIT %s
        """, (common_name_of_animal, top_n))
        return cursor.fetchall()

    def getTopSpeciesByCity(self, city_name, radius_miles=10, top_n=3):
        """Returns top species near a city name string."""
        coords = forward_geocode(city_name)
        if coords is None:
            return city_name, None
        lat, lon = coords
        return city_name, self.getTopSpeciesNear(lat, lon, radius_miles, top_n)


def forward_geocode(city_name):
    """Converts a city name to (lat, lon) using Nominatim."""
    url = "https://nominatim.openstreetmap.org/search"
    params  = {"q": city_name, "format": "json", "limit": 1}
    headers = {"User-Agent": "ind-flask-jtvaughn/1.0"}
    resp = requests.get(url, params=params, headers=headers)
    if resp.ok:
        results = resp.json()
        if results:
            return float(results[0]["lat"]), float(results[0]["lon"])
    return None