from tkinter import *
import json
from time import sleep
from functools import partial
import RPi.GPIO as GPIO # type: ignore
import config
from drinks import startDrink

# Constants
BUTTON_COLOR = "#1a70d9"
BUTTON_COLOR_ACTIVE = "#5ac92e"
BACK_COLOR = "#b52619"
BACKGROUND_COLOR = "#2b2b2b"


# Initialization
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
wn.geometry("600x1024")
wn.configure(background=BACKGROUND_COLOR)
#wn.overrideredirect(True)
wn.attributes("-fullscreen", 1)


# Global variables
globalPickedDrink = None
drinkButtons = []
volumeButtons = []
backButton = None

# Functions for changing the layout for choosing drinks or volumes
def selectVolumes(drink):
    global globalPickedDrink
    globalPickedDrink = drink

    for i, b in enumerate(drinkButtons):
        b.grid_forget()
    for i, b in enumerate(volumeButtons):
        b.grid(column=0, row=(i + 1) * 2, rowspan=2, padx=10, pady=10)

    backButton.grid(column=0, row=0, rowspan=2, padx=10, pady=10)

def selectGlasses():
    global globalPickedDrink
    globalPickedDrink = None

    for i, b in enumerate(drinkButtons):
        b.grid(column=0, row=i, padx=10, pady=10)
    for i, b in enumerate(volumeButtons):
        b.grid_forget()

    backButton.grid_forget()

backButton = Button(wn, text=f"Back", font=("Arial", 20, "bold"), command=selectGlasses, height=4, width=100, highlightthickness=0, border=0, bg=BACK_COLOR, activebackground=BUTTON_COLOR_ACTIVE)


# Create the buttons
drinkListLength = len(data["drinks"])
for i in range(0,drinkListLength):
    drink = data["drinks"][i]

    # Create the button for a drink
    drinkButton = Button(wn, text=drink["name"], font=("Arial", 20, "bold"), command=partial(selectVolumes, drink), height = 3, width=100, highlightthickness=0, border=0, bg=BUTTON_COLOR, activebackground=BUTTON_COLOR_ACTIVE)
    drinkButton.grid(column=0, row=i, padx=10, pady=10)

    # Make the button-grid span the entire width
    wn.columnconfigure(i, weight=1)

    drinkButtons.append(drinkButton)

# Create Volume buttons, and then hide them
for i, volume in enumerate(glassVolumes):
    def confirm(volume):
        startDrink(globalPickedDrink, data, conf, volume)

        selectGlasses()

    b = Button(wn, text=f"{volume}ml", font=("Arial", 20, "bold"), command=partial(confirm, volume), height=4, width=100, highlightthickness=0, border=0, bg=BUTTON_COLOR, activebackground=BUTTON_COLOR_ACTIVE)
    b.grid(column=0, row=i, rowspan=2, padx=10, pady=10)

    volumeButtons.append(b)

    b.grid_forget() # Hide it



# Loop to maintain the window
mainloop()

GPIO.cleanup()