#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from rpi_ws281x import *
import argparse
import math
from w1thermsensor import W1ThermSensor
sensor = W1ThermSensor()

MAX_TEMP = 100
MIN_TEMP = 0


# LED strip configuration:
LED_COUNT      = 300      # Number of LED pixels.
MAX_COLOR_LED = 200
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

def getColor(lednr):
    red = math.floor(lednr/MAX_COLOR_LED * 255)
    print("red is",red)
    print("lednr is",lednr)
    if red > 255:
        red = 255

    blue = 255-red

    if blue > red:
        green = 255 - blue
    else:
        green = 255 -red
        red = 255
        blue = 0
   
    return Color(red,green,blue)
    
def SetColor(temp):
    nr_of_leds =math.floor(LED_COUNT*temp/MAX_TEMP)
    print("nr of leds is",nr_of_leds)
    for i in range(0,LED_COUNT):
        if i <nr_of_leds:
            color = getColor(i)
        else:
            color = Color(0,0,0)
        strip.setPixelColor(i,color)
        strip.show()


# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        while True:
            SetColor(math.floor(sensor.get_temperature()))
            time.sleep(15)
          

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)
