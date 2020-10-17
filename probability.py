import numpy as np
from datetime import datetime, date, time
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

distanceList = []
M = 0
probForDist = 0

sumDistance = 0
for item in distance:
    sumDistance += item
    distanceList.append(item)

probabilityForNearestDist = nearestDist / sumDistance

def countMathExpect():
    for item in distanceList:
        ver = item / sumDistance
        M += ver * item
    return M
