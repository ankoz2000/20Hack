from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import csv
import  datetime

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
        else:
            current = geodesic(point, (loc.latitude, loc.longitude)).miles
            if current < smallest:
                smallest = current
    return smallest

def getTime():
    return date

def countTimeDiff(user):
    now = datetime.datetime.today()
    d = user.day
    mo = user.month
    y = user.year
    h = user.h
    mins = user.m
    s = user.s

    last = datetime.datetime(y, mo, d, h, mins, s)  # Время когда костыльный больной юзер
                                                    # находился (находится) на территории

    delta = now - last
    hours = delta.seconds // 3600
    minutes = delta.seconds % 3600 // 60
    str = "{} дней {} часов {} минут".format(delta.days, hours, minutes)

    return [delta, str]

def countIllDist(health, ill):
    dist = geodesic(health, ill).miles


#def countTime():

