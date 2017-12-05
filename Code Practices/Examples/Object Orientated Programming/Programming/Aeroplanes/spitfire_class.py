'''Spitfire class inherits from Aeroplane class
Les Timms
22/05/2017'''

from aeroplane_class import *

class Spitfire(Aeroplane):

    def __init__(self):
        # constructor line - notice 'self' plus all the arguments needed
        self.name = "Spitfire"                    # attributes set to initial values
        self.wing_type = "monoplane"
        self.engine_type = "piston"
        self.max_speed = 365

    def max_diving_speed(self):
        # this does not appear in the parent (aeroplane) class
        print("Max safe diving speed", round(self.max_speed * 1.4,0), "mph")

    
