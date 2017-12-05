import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.IN)

GPIO.setup(16, GPIO.OUT)

GPIO.output(16, False)
            

while True:   
        
    GPIO.output(16, True)
    time.sleep(0.00001)
    GPIO.output(16, False)

    while GPIO.input(20)==0:
        pulse_start = time.time()

    while GPIO.input(20)==1:
        pulse_end = time.time()


    pulse_duration = pulse_end - pulse_start
    duration = pulse_duration / 2
    distance = pulse_duration * 34300
    distance = round(distance, 2)
    print(distance)
    time.sleep(0.5)
