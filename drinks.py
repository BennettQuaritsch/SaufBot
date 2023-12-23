import RPi.GPIO as GPIO # type: ignore
import threading
from functools import partial
import ledring
from time import sleep

# Start lightstrip
lstrip = ledring.startStrip()

def openPump(ingredient, data, conf, pickedVolume):
    tt100 = data["timeFor100ml"]

    hose = next(hose[ingredient["ingredient"]] for hose in data["hoseConfig"] if ingredient["ingredient"] in hose)
    pump = next(pump for pump in conf.pumpList if pump.hose == hose)

    GPIO.output(pump.gpio, 0) # Open pump

    timeToSleep = (tt100 / 100) * pickedVolume * (ingredient["volumePercentage"] / 100)
    sleep(timeToSleep)

    GPIO.output(pump.gpio, 1) # Close Pump

def startDrink(drink, data, conf, pickedVolume): #, volumeSelectionPopup):
    #print(f"drink: {drink["name"]}")
    tt100 = data["timeFor100ml"]
    
    # pickedVolume = volumeSelectionPopup()
    
    print(pickedVolume)
    if pickedVolume is None: return # Check if a volume was picked

    maxTime = 0

    for ingredient in drink["ingredients"]:
        timeToSleep =  (tt100 / 100) * pickedVolume * (ingredient["volumePercentage"] / 100)
        if timeToSleep > maxTime:
            maxTime = timeToSleep
    
    lightThread = threading.Thread(target=ledring.progressRing, args=(lstrip, maxTime))
    lightThread.start()

    pumpThreads = [] # Threading, so each pump works simoultaneously
    
    for ingredient in drink["ingredients"]:
        #print(f"ingredient: {ingredient["ingredient"]}")

        pumpThread = threading.Thread(target=openPump, args=(ingredient, data, conf, pickedVolume))
        pumpThread.start()
        pumpThreads.append(pumpThread)

    for pumpThread in pumpThreads:
        pumpThread.join()

    lightThread.join()

    ledring.blinkStrip(lstrip)

    ledring.endStrip(lstrip)