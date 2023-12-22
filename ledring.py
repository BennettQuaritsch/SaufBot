import time
from rpi_ws281x import PixelStrip, Color
import argparse

# LED strip configuration:
LED_COUNT = 18      # Number of LED pixels.
LED_PIN = 12          # GPIO pin connected to the pixels (12 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0     # set to '1' for GPIOs 13, 19, 41, 45 or 53


def startStrip():
    # Create NeoPixel object with appropriate configuration.
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    return strip

def progressRing(strip, maxTime):
    timePerPixel = maxTime / LED_COUNT
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0,255,0))
        strip.show()
        time.sleep(timePerPixel)

def blinkStrip(strip, interval=0.2, blinkNum=5):
    for i in range(blinkNum):
        for j in range(strip.numPixels()):
            strip.setPixelColor(j, Color(0,0,0))

        strip.show()

        time.sleep(interval)

        for j in range(strip.numPixels()):
            strip.setPixelColor(j, Color(0,255,0))

        strip.show()

        time.sleep(interval)


def endStrip(strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0,0,0))
        strip.show()