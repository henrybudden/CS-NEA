##              ____________ 
##           2 /            \ 3 
##            |              |
## Front      |              |        Rear
##            |              | 
##           1 \____________/ 4
##
import random

class distance():
    def __init__(self):
        self.distances = {
            1:0,
            2:0,
            3:0,
            4:0
            }

    def setup(self):
        pass
            
    def get_distance_all(self):
        for sensor in range(1,5):
            distance = random.randint(1,50)
            self.distances[sensor] = distance
        return self.distances
            
            
    


