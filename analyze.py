from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import csv

date = []
addresses = []
csv_path = "lite.csv"


def csv_reader(file_obj):
    """
    Read a csv file
    """
    reader = csv.DictReader(file_obj, delimiter=';')
    for row in reader:
        date.append(row['date'])
        addresses.append(row['address'])
        print(row)
    return {"date": date, "address": addresses}


geolocator = Nominatim(user_agent="my-app")


def countDistance(point):
    with open(csv_path, "r") as file:
        dict = csv_reader(file)
    location = geolocator.geocode(dict['address'][0])
    smallest = geodesic(point, location).miles
    Fails = []

    for obj in dict['address']:
        loc = geolocator.geocode(obj)
        if loc == None:
            Fails.append(obj)
            print(obj)
        else:
            current = geodesic(point, (loc.latitude, loc.longitude)).miles
            if current < smallest:
                smallest = current
                print(obj)
    return smallest
