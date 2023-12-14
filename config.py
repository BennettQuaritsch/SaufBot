import json

class Config():
    def __init__(self, ledGPIO, pumpList):
        self.ledGPIO = ledGPIO
        self.pumpList = pumpList

class Pump():
    def __init__(self, hose, gpio):
        self.hose = hose
        self.gpio = gpio
    

# Read json config file
f = open("config.json")
data = json.loads(f.read())


def loadConfig():
    ledGPIO = data["ledGPIO"]

    pumpList = []
    for pump in data["pumps"]:
        pumpList.append(Pump(hose=pump["hose"], gpio=pump["gpio"]))

    conf = Config(ledGPIO=ledGPIO, pumpList=pumpList)

    return conf
    