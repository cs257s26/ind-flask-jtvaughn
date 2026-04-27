"""Finds most observed species near a location in Minnesota."""

import csv
import os
import requests
import sys
from collections import defaultdict, Counter
import argparse


from math import radians, sin, cos, sqrt, atan2

DATA_DIR = "ProductionCode/data"

TAXA = ["amphibians", "birds", "insects", "mammals", "reptiles"]


def load_data():
    """Loads all taxon CSVs into data as lists of dicts."""
    data={}
    for taxon in TAXA:
        filepath = os.path.join(DATA_DIR, f"{taxon}.csv")
        with open(filepath, newline='') as f:
            data[taxon] = list(csv.DictReader(f))
    return data

def reverse_geocode(lat, lon):
    """ Returns a real location name for coordinates
    
    Args:
    lat: Latitude as a float
    lon: Longitude as a float

    Returns
    String location like "Northfield, Minnesota"
    """
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {"lat": lat, "lon": lon, "format": "json"}
    headers = {"User-Agent": "project-g/1.0"}
    resp = requests.get(url, params=params, headers=headers)
    if resp.ok:
        addr = resp.json().get("address", {})
        city = addr.get("city") or addr.get("town") or addr.get("village")
        state = addr.get("state")
        return f"{city}, {state}" if city else state
    return None

def forward_geocode(city_name):
    """Converts a city name to coordinates.
    
    Args:
        city_name: A string like "Nothfield, Minnesota"
    
    Returns:
        (lat, lon) tuple of floats, or None if lookup fails. 7 decimal places
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": city_name, "format": "json", "limit": 1}
    headers = {"User-Agent": "project-g/1.0"}
    resp = requests.get(url, params=params, headers=headers)
    if resp.ok:
        results = resp.json()
        if results:
            return float(results[0]["lat"]), float(results[0]["lon"])
    return None

def haversine_miles(lat1, lon1, lat2, lon2):
    """Calculates the great-circle distance between two points in miles.
    
    Args:
        lat1, lon1: Latitude and longitude of the first point in decimal degrees
        lat2, lon2: Latitude and longitude of the second point in decimal degrees
    
    Returns:
        Distance in miles as a float
    
    References:
        Sinnott, R.W. (1984). Virtues of the Haversine. Sky and Telescope, 68(2), 159.
    """
    R = 3958.8  # Earth radius in miles
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))

def filter_by_radius(data, lat, lon, radius_miles=10):
    """ Filters observations to those within a radius of given coordinates.
    
    Args:
        data: Dict of taxon to list of observation dicts, each with 'latitude' and 'longitude' keys
        lat: Latitude of center point as float
        lon: Longitude of center point as float
        radius_miles: Radius in miles to filter by (default: 10)
    Returns:     List of observation dicts within the specified radius
    """
    results = []
    for taxon_rows in data.values():
        for row in taxon_rows:
            try:
                obs_lat = float(row["latitude"])
                obs_lon = float(row["longitude"])
                if haversine_miles(lat, lon, obs_lat, obs_lon) <= radius_miles:
                    results.append(row)
            except (ValueError, KeyError):
                continue
    return results

def top_species_by_taxon(observations, top_n=3):
    """Returns the top N most observed species grouped by iconic taxon.
    
    Args:
        observations: List of dicts from DictReader, each containing
            'iconic_taxon', 'taxon_name', and 'common_name' keys
        top_n: Number of top species to return per taxon group, defaults to 3
    
    Returns:
        Dict mapping iconic_taxon string to list of (taxon_name, common_name, count)
        tuples sorted by count descending
    """
    grouped = defaultdict(list)
    for row in observations:
        grouped[row["iconic_taxon"]].append(row)
    
    result = {}
    for taxon_group, rows in grouped.items():
        counts = Counter(row["taxon_name"] for row in rows)
        name_map = {}
        for row in rows:
            if row["taxon_name"] not in name_map:
                name_map[row["taxon_name"]] = row["common_name"]
        result[taxon_group] = [
            (taxon, name_map[taxon], count)
            for taxon, count in counts.most_common(top_n)
        ]
    
    return result

def main():
    parser = argparse.ArgumentParser(description="Find commonly observed species near a location in Minnesota")
    parser.add_argument("city", type=str, help="City name to search near, e.g. 'Northfield, Minnesota'")
    parser.add_argument("--radius", type=float, default=10, help="Search radius in miles (default: 10)")
    parser.add_argument("--top", type=int, default=3, help="Number of top species per taxon (default: 3)")
    args = parser.parse_args()

    data=load_data()
    coords = forward_geocode(args.city)
    if coords is None:
        print(f"Could not geocode '{args.city}'")
        sys.exit(1)
    lat, lon = coords
    observations = filter_by_radius(data, lat, lon, args.radius)
    if len(observations) == 0:
        print(f"No observations found near '{args.city}'. Make sure your location is in Minnesota.")
        sys.exit(1)
    print(f"Found {len(observations)} observations within {args.radius} miles of {args.city}:")
    top_by_taxon = top_species_by_taxon(observations, args.top)
    for taxon_group, species_list in top_by_taxon.items():
        print(f"\n{taxon_group.capitalize()}:")
        for taxon_name, common_name, count in species_list:
            print(f"{common_name} ({taxon_name}): {count} observations")


if __name__ == "__main__":
    main()