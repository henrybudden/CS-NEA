from databaseClass import *
from shortestClass import *
import operator
db = Database()
sh = ShortestPath()

class Improvements():

    def __init__(self):
        pass

    def get_improvements(self):
        improvedict = {}
        data = db.get_order_analysis()
        used = db.get_used_locations()
        unused = ['A1', 'A2', 'A3', 'A4', 'A5', 'B1', 'B2', 'B3', 'B4', 'B5', 'C1', 'C5', 'D1', 'D2', 'D3', 'D4', 'D5', 'E1', 'E2', 'E3', 'E4', 'E5', 'F1', 'F5', 'G1', 'G2', 'G3', 'G4', 'G5', 'H1', 'H2', 'H3', 'H4', 'H5']
        for x in used:
            for i in unused:
                if x == i:
                    unused.remove(x)
        unuseddict = {}
        for x in unused:
            unuseddict[x] = sh.get_distance("I2", x)
        unuseddict = sorted(unuseddict.items(), key=operator.itemgetter(1))
        for x in data[2]:
            current_location = db.get_item_singleinfo(x[0], "ItemLocation")
            current_distance = sh.get_distance("I2", current_location)
            try:
                nearest_avaliable = unuseddict[0][0]
            except:
                print("No More Avaliable Locations")
                break
            if unuseddict[0][1] < current_distance:
                #print(current_location, "->", nearest_avaliable)
                improvedict[current_location] = nearest_avaliable
                del(unuseddict[0])
            else:
                pass
                #print(current_location, "->", current_location)
        return(improvedict)
   
