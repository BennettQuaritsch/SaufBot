from tkinter import *
import json
from functools import partial
from time import sleep
import RPi.GPIO as GPIO
import config

GPIO.setmode(GPIO.BOARD)

# Read config
conf = config.loadConfig()

for pump in conf.pumpList:
    GPIO.setup(pump.gpio, GPIO.OUT, initial=GPIO.HIGH)


# Read json drinks file
f = open("drinks.json")
data = json.loads(f.read())

# Read time to fill 100 ml
tt100 = data["timeFor100ml"]

glassVolumes = data["glassVolumes"]

# Initialize the main window
wn = Tk()
wn.title("PiCocktailMaker")
wn.geometry("480x800")
wn.configure(background="#2b2b2b")

pickedVolume = None

def someFunc(drink):
    #print(f"drink: {drink["name"]}")
    
    def dismiss():
        global pickedVolume
        pickedVolume = None

        dialog.grab_release()
        dialog.destroy()
        return

    def confirmVolume(vol):
        global pickedVolume
        pickedVolume = vol

        dialog.grab_release()
        dialog.destroy()
    
    # Create popver
    dialog = Toplevel(wn)
    dialog.title("Glas Größe")
    dialog.geometry("480x300")

    # Create Volume buttons in popover
    for i, volume in enumerate(glassVolumes):
        Button(dialog, text=f"{volume}ml", command=partial(confirmVolume, volume), height=10, width=100).grid(column=i, row=0)

        dialog.columnconfigure(i, weight=1)

    # Configure window position to be inside the original window
    x = wn.winfo_x()
    y = wn.winfo_y()
    dialog.geometry(f"+{x}+{y+200}")

    dialog.protocol("WM_DELETE_WINDOW", dismiss)
    dialog.transient(wn)
    dialog.wait_visibility()
    dialog.grab_set()
    
    dialog.wait_window() # Wait until popover is closed
    print(pickedVolume)
    if pickedVolume is None: return # Check if a volume was picked
    
    for ingredient in drink["ingredients"]:
        #print(f"ingredient: {ingredient["ingredient"]}")

        hose = next(hose[ingredient["ingredient"]] for hose in data["hoseConfig"] if ingredient["ingredient"] in hose)
        pump = next(pump for pump in conf.pumpList if pump.hose == hose)

        GPIO.output(pump.gpio, 0) # Open pump

        timeToSleep = (tt100 / 100) * pickedVolume * (ingredient["volumePercentage"] / 100)
        sleep(timeToSleep)

        GPIO.output(pump.gpio, 1) # Close Pump

# Create the buttons
drinkListLength = len(data["drinks"])

for i in range(0,drinkListLength):
    drink = data["drinks"][i]

    # Create the button for a drink
    someButton = Button(wn, text=drink["name"], command=partial(someFunc, drink), height = 4, width=100, highlightthickness=0, border=0, bg="yellow", activebackground="red")
    someButton.grid(column=0, row=i, padx=10, pady=10)

    # Make the button-grid span the entire width
    wn.columnconfigure(i, weight=1)

# Loop to maintain the window
mainloop()

GPIO.cleanup()