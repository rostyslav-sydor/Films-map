"""
A program that shows locations nearby where films were shot.
"""


import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable
from geopy.distance import geodesic
from math import asin, cos, sin, sqrt
import folium

def readFile(path: str, year: str) -> list:
    """
    Returns list of all strings with [year].
    """
    with open(path, encoding='latin1') as locations:
        locs = []
        found_locs = set()
        for i, line in enumerate(locations):
            if ('('+year+')') in line and line.split('\t')[0] not in found_locs:
                line = line.strip('\n').split('\t')
                locs.append(list(filter(None, line)))
                found_locs.add(locs[-1][0])
    return locs[::len(locs)//100]


def findCoords(locations: list) -> list:
    """
    Finds coords of all locations from list.
    """
    print("Map is generating...")
    geolocator = Nominatim(user_agent='hello')
    coords = []
    good_locations = []
    for i, line in enumerate(locations):
        if i == len(locations)//2:
            print("Please wait...")
        try:
            location = geolocator.geocode(line[1])
            location.latitude
            coords.append((location.latitude, location.longitude))
            good_locations.append(line[0])
        except (AttributeError, GeocoderUnavailable):
            pass
    return coords, good_locations


def calculateDistance(startingPoint: tuple, coords: list) -> list:
    """
    Calculates distances between starting point and every locations from coords.
    """
    radius = 6371
    lat1 = startingPoint[0]
    longt1 = startingPoint[1]
    distances = []
    for line in coords:
        lat2 = line[0]
        longt2 = line[1]
        diff_lat = lat2 - lat1
        diff_long = longt2 - longt1
        pip = (sin(diff_lat/2)**2) + cos(lat2)*cos(lat1)*(sin((diff_long)/2)**2)
        dist = geodesic(startingPoint, line).km
        distances.append(dist)
    return distances


def main(startingPoint: tuple, year: str):
    """
    Main function that does all the stuff and generates Map.html
    """
    locations = readFile('locations.list', year)
    coords, locations = findCoords(locations)
    distances = calculateDistance(startingPoint, coords)
    allBlue = list(zip(locations, coords, distances))
    karta = folium.Map()
    allBlue = sorted(allBlue, key=lambda x: x[2])
    for line in allBlue[:15]:
        karta.add_child(folium.Marker(location=[line[1][0], line[1][1]], popup=line[0]))
    karta.save("Map.html")


if __name__ == "__main__":
    try:
        year = input("Hello user!\nPlease enter year of films you want: ")
        lat = float(input("Now enter your latitude: "))
        longt = float(input("And now enter your longtitude: "))
        main((lat, longt), year)
        print("Your map is ready, have a look!")
    except (AttributeError, TypeError):
        print("You've entered something wrong, try again.")


