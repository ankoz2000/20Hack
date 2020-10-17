from geopy.distance import geodesic
from geopy.geocoders import Nominatim, ArcGIS
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
    return {"date": date, "address": addresses}


#geolocator = Nominatim(user_agent="my-app")
geolocator = ArcGIS()


def countDistance(point):
    with open(csv_path, "r") as file:
        dict = csv_reader(file)
    location = geolocator.geocode(dict['address'][0])
    smallest = geodesic(point, location).miles * 1.609344  # Перевод в километры
    Fails = []
    sickQuantity = 0

    for obj in dict['address']:
        loc = geolocator.geocode(obj)
        if loc == None:
            Fails.append(obj)
        else:
            current = geodesic(point, (loc.latitude, loc.longitude)).miles * 1.609344  # Перевод в километры
            if isIncludes(current):
                sickQuantity += 1
            if current < smallest:
                smallest = current
    return smallest

def getTime():
    return date

def countTimeDiff(user):
    sickQuantity = 0
    Fails = []

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

    with open(csv_path, "r") as file:
        dict = csv_reader(file)
    for obj in dict['address']:
        loc = geolocator.geocode(obj)
        if loc == None:
            Fails.append(obj)
        else:
            current = geodesic((user.lt, user.lg), (loc.latitude, loc.longitude)).miles * 1.609344  # Перевод в километры
            if isIncludes(current):
                sickQuantity += 1

    return [delta, str, sickQuantity]


def isIncludes(distance):
    radius = 3  # km
    return distance <= radius


def countIllDist(health, ill):
    dist = geodesic(health, ill).miles


#def countTime():

