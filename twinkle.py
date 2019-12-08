import RPi.GPIO as GPIO
import random
from time import sleep

GPIO.setmode(GPIO.BCM)

pins = [17, 22, 23, 24,]

for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

last = 17
t_pin = 17

while True:
    sleep(random.uniform(0, 1.5))
    while (t_pin != last):
         t_pin = random.choice(pins)
    last = t_pin
    GPIO.output(t_pin, GPIO.LOW)
    sleep(0.05)
    GPIO.output(t_pin, GPIO.HIGH)
