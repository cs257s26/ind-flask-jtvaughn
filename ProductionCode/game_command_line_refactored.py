import argparse
import csv
import random
from collections import Counter
import os

import csv
import os
import requests
from collections import defaultdict, Counter
import argparse


from math import radians, sin, cos, sqrt, atan2

currentFolder = os.path.dirname(os.path.abspath(__file__))
projectRoot = os.path.dirname(currentFolder)
FILEPATH = os.path.join(projectRoot, 'ProductionCode', 'data')

def load_data():
    '''Loads in data from CSV files and returns a flat list of dicts'''
    data = []
    for filename in os.listdir(FILEPATH):
        if filename.endswith(".csv"):
            with open(os.path.join(FILEPATH, filename), newline='') as datafile:
                csv_file = csv.DictReader(datafile) 
                for row in csv_file:
                    data.append(row)
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


def makeRandomLocation(data):
    '''Returns a random city/state string by reverse geocoding a random observation's coordinates'''
    rowCount=len(data)
    randomLine = random.randint(0, rowCount - 1) #get a random line from the CSV
    Lat = data[randomLine]["latitude"] 
    Lon = data[randomLine]["longitude"] 
    makeRandomLocation = reverse_geocode(float(Lat), float(Lon)) 
    return makeRandomLocation

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
        data: Flat list of observation dicts, each with 'latitude' and 'longitude' keys
        lat: Latitude of center point as float
        lon: Longitude of center point as float
        radius_miles: Radius in miles to filter by (default: 10)
    Returns:     List of observation dicts within the specified radius
    """
    results = []
    for row in data:  
        try:
            obs_lat = float(row["latitude"])
            obs_lon = float(row["longitude"])
            if haversine_miles(lat, lon, obs_lat, obs_lon) <= radius_miles:
                results.append(row)
        except (ValueError, KeyError):
            continue
    return results

def makeRandomLocationList(results)-> list:   
    '''Takes a Counter of species counts and returns a sorted list of (species, count) tuples'''
    mostCommon = results.most_common()
    return mostCommon

def getCorrectAnswers(mostCommon: list) -> tuple[str, str]:
    '''Gets the most common animal and it's sighting frequency and sets that to be the correct answer. '''
    correctAnswer = mostCommon[0]
    correctAnswerAnimal = correctAnswer[0]
    correctAnswerCount = correctAnswer[1]
    return correctAnswerAnimal, correctAnswerCount

def top5AnimalsList(mostCommon: list)-> list[list]: 
    '''Makes a new list of just the top 5 animals then shuffles. '''
    top5Animals = mostCommon[0:5]
    random.shuffle(top5Animals)
    return top5Animals

def game(data):
    '''This function will have randomly choose a location
    and players will need to choose from 5 options which the most common animal reported at that location. '''
    randomLocationName = makeRandomLocation(data)
    coords = forward_geocode(randomLocationName)
    lat, lon = coords
    results = filter_by_radius(data, lat, lon)
    species_counts = Counter(row["common_name"] for row in results if row["common_name"])
    mostCommon = makeRandomLocationList(species_counts)
    top5Animals = top5AnimalsList(mostCommon)
    correctAnswerAnimal, correctAnswerCount = getCorrectAnswers(mostCommon)
    
    '''
    print("Which is the most commonly reported species in ", randomLocationName, "?")
    print("Choose one: ", ", ".join(animal[0] for animal in top5Animals))
    userAnswer = input("Type your guess here: ")
    if correctAnswerAnimal == userAnswer:
        print("Correct!")
    else:
        print("Incorrect, the most commonly reported animal is: ", correctAnswerAnimal, ", reported ", correctAnswerCount, " times.")
    '''

    return {
        "location": randomLocationName,
        "options": (animal[0] for animal in top5Animals),
        "correctAnimal": correctAnswerAnimal,
        "correctCount": correctAnswerCount
    }

def main():
    data= load_data()
    parser = argparse.ArgumentParser()
    parser.add_argument("game")
    game(data)

if __name__=='__main__':
    main()


  