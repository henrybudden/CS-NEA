class Animal:
    def __init__(self, name, s, n):
        self.state = s
        self.size = n
        self.name = name

    def feed(self):
        self.size = self.size + 1
        if self.size == 5:
            self.state = "FISH"

    def getName(self):
        return self.name

    def getState(self):
        return self.state

    def getSize(self):
        return self.size

class Fishbowl:
    def __init__(self, names):
        self.names = names 

    def feedAll(self):
        for x in self.names:
            while x.getState() != "FISH":
                x.feed()
                print(x.getName(), "has been fed")
            




dave = Animal("Dave", "fish", 1)
pete = Animal("Pete", "fish", 2)
fish = [dave, pete]
houseofcommons = Fishbowl(fish)
houseofcommons.feedAll()



