import random

class Crop:
    """A generic food crop"""
    
    #constructor
    def __init__(self, growth_rate, light_need, water_need):

        #set attributes with initial values. Underscore prefix denotes protected attribute
        self._growth = 0
        self._days_growing = 0
        self._growth_rate = growth_rate
        self._light_need = light_need
        self._water_need = water_need
        self._status = "Seed"
        self._type = "Generic"

    def needs(self):
        #return a dictionary containing light and water needs
        return {"Light Need": self._light_need,
                "Water Need": self._water_need
                }
    
    def report(self):
        #retun a dictionary containing the type, status, growth rate and days growing
        return{"Type": self._type,
               "Status": self._status,
               "Growth Rate": self._growth_rate,
               "Days Growing": self._days_growing
               }

    def _update_status(self):
        if self._growth > 15:
            self._status = "Old"
        elif self._growth > 10:
            self._status = "Mature"
        elif self._growth > 5:
            self._status = "Young"
        elif self._growth > 0:
            self._status = "Seedling"
        elif self._growth == 0:
            self._status = "Seed"

    def grow(self, light, water):
        if light >= self._light_need and water >= self._water_need:
            self._growth += self._growth_rate
        #increment days growing
        self._days_growing += 1
        #update status
        self._update_status()

def auto_grow(crop, days):
    #grow the crop
    for day in range(days):
        light = random.randint(1,10)
        water = random.randint(1,10)
        crop.grow(light, water)

def manual_grow(crop):
    #get the light and water values from the user
    valid = False
    while not valid:
        try:
            light = int(input("Please enter a light value (1-10): "))
            if light >= 1 and light <= 10:
                valid = True
            else:
                print("Value entered not valid - please enter a value between 1 and 10")

        except ValueError:
            print("Value entered not valid - please enter a value between 1 and 10")


def main():
    #instantiate the class
    new_crop = Crop(1,4,3)
    print(new_crop.needs())
    print(new_crop.report())
    auto_grow(new_crop, 30)
    print(new_crop.report())


if __name__ == "__main__":
    main()
