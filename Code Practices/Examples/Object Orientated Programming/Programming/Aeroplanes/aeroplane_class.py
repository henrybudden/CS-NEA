'''OOP demonstrator - aeroplane class
Les Timms
22/05/2017'''

class Aeroplane:    # creates aeroplane class
    aircraft_total = 0  # initialises value
    
    def __init__(self,name,wing_type,engine_type, max_speed):
        # constructor line - notice 'self' plus all the arguments needed
        self.name = name                    # attributes set to initial values
        self.wing_type = wing_type
        self.engine_type = engine_type
        self.max_speed = max_speed
        Aeroplane.aircraft_total += 1       # increments by 1 every time a new object is created     

    def info(self):                         # a method to display data
        print("Type is",self.name)
        print("Wing configuration:",self.wing_type)
        print("Engine type:",self.engine_type)
        print("Max speed is", self.max_speed, "mph")
               
    def diving_speed(self,angle):           # a method to perform a calculation
        if angle >= 30:
            self.diving_speed = ((self.max_speed + angle*2)/self.max_speed)* self.max_speed
            print("Diving speed:",self.diving_speed, "mph")
            if self.diving_speed > self.max_speed * 1.4:
                print("Pull up, too fast!")
        print("*" * 40)

    def climbing_speed(self, angle):
        if angle > 60:
            print("Go down, too steep!")
        self.climbing_speed = ((self.max_speed)*((((90-angle)/90))))
        print("Climbing speed:",self.climbing_speed, "mph")
            

spit = Aeroplane("spitfire","monoplane", "piston", 365) # instantiation of spitfire object
spit.info()
spit.climbing_speed(90)                                 # retrieves data from class
spit.diving_speed(70)                                   # uses diving_speed method

print("Total number of aircraft", Aeroplane.aircraft_total)

# 1. Create a new method to show the climbing speed dependent on the angle
# 2. Instantiate the Gladiator (a slow biplane) and display the same info as for Spitfire


        


