class Animal:
    def __init__(self, s, n):
        self._state = s
        self._size = n

    def feed(self):
        self._size += 1
        print(self._state, "fed")

    def getState(self):
        return self._state

    def getSize(self):
        return self._size

class Fish(Animal):
    def __init__(self, s):
        Animal.__init__(self, s, 1)
        self.maxSize = 2
        
    def setMaxSize(self, n):
        self.maxSize = n
        
    def feed(self):
        self._size += 2
        print(self._state, "fed")
        if self._size >= self.maxSize:
            self._state = "BIG FISH"
           

class Duck(Animal):
    def __init__(self, s):
        Animal.__init__(self, s, 3)
    def feed(self):
        Animal.feed(self)
        if self._size == 5:
            self._state = "BIG DUCK" 

thisFish = Fish("little fish")
thisFish.setMaxSize(3)
thisDuck = Duck("little duck")
for count in range(0,3):
    thisDuck.feed()
    print(thisDuck.getState())
    thisFish.feed()
    print(thisFish.getState())
