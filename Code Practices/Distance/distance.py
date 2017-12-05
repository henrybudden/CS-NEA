##              ____________ 
##           2 /            \ 3 
##            |              |
## Front      |              |        Rear
##            |              | 
##           1 \____________/ 4
##
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

class distance():
    def __init__(self):
        self.trig1 = 19
        self.echo1 = 26
        self.trig2 = 17
        self.echo2 = 27
        self.trig3 = 24
        self.echo3 = 23
        self.trig4 = 21
        self.echo4 = 20
        self.inpins = [self.echo1,self.echo2,self.echo3,self.echo4]
        self.outpins = [self.trig1,self.trig2,self.trig3,self.trig4]
        self.allpins = {
            self.trig1:self.echo1,
            self.trig2:self.echo2,
            self.trig3:self.echo3,
            self.trig4:self.echo4
            }
        self.distances = {
            1:0,
            2:0,
            3:0,
            4:0
            }

    def setup(self):
        for x in self.inpins:
            #print(x)
            GPIO.setup(x, GPIO.IN)

        for x in self.outpins:
            #print(x)
            GPIO.setup(x, GPIO.OUT)

        for x in self.outpins:
            #print(x)
            GPIO.output(x, False)
            

    def get_distance_all(self):
        for x in self.allpins:
            if x == self.trig1:
                sensor = 1
            elif x == self.trig2:
                sensor = 2
            elif x == self.trig3:
                sensor = 3
            elif x == self.trig4:
                sensor = 4
            
            GPIO.output(x, True)
            time.sleep(0.00001)
            GPIO.output(x, False)

            while GPIO.input(self.allpins[x])==0:
                pulse_start = time.time()

            while GPIO.input(self.allpins[x])==1:
                pulse_end = time.time()
            

            pulse_duration = pulse_end - pulse_start
            duration = pulse_duration / 2
            distance = pulse_duration * 34300
            distance = round(distance, 2)
            self.distances[sensor] = distance
        return self.distances
            


dist = distance()
dist.setup()
while True:
    time.sleep(0.5)
    print(dist.get_distance_all())
            
    


