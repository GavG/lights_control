import RPi.GPIO as GPIO
import random
from time import sleep

GPIO.setmode(GPIO.BCM)

pins = [17, 22, 23, 24,]

for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

while True:
    sleep(random.uniform(0, 1.5))
    t_pin = pins[random.randint(0, 3)]
    GPIO.output(t_pin, GPIO.LOW)
    sleep(0.05)
    GPIO.output(t_pin, GPIO.HIGH)
