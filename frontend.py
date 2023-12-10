from tkinter import *
import json
from functools import partial
from time import sleep

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

def someFunc(drink):
    print(f"drink: {drink["name"]}")
    pickedVolume = glassVolumes[0]

    def dismiss():
        dialog.grab_release()
        dialog.destroy()
        return

    def confirmVolume(vol):
        pickedVolume = vol

        dialog.grab_release()
        dialog.destroy()

    dialog = Toplevel(wn)
    dialog.title("Glas Größe")
    dialog.geometry("480x300")

    for i, volume in enumerate(glassVolumes):
        Button(dialog, text=f"{volume}ml", command=partial(confirmVolume, volume), height=10, width=100).grid(column=i, row=0)

        dialog.columnconfigure(i, weight=1)

    x = wn.winfo_x()
    y = wn.winfo_y()
    dialog.geometry(f"+{x}+{y+200}")

    dialog.protocol("WM_DELETE_WINDOW", dismiss)
    dialog.transient(wn)
    dialog.wait_visibility()
    dialog.grab_set()

    dialog.wait_window()
    
    for ingredient in drink["ingredients"]:
        print(f"ingredient: {ingredient["ingredient"]}")
        # Open the corresponding pump
        timeToSleep = (tt100 / 100) * pickedVolume * (ingredient["volumePercentage"] / 100)
        sleep(timeToSleep)
        # Close the pump

# Create the buttons
drinkListLength = len(data["drinks"])

for i in range(0,drinkListLength):
    drink = data["drinks"][i]

    # Create the button for a drink
    someButton = Button(wn, text=f"{drink["name"]}", command=partial(someFunc, drink), height = 4, width=100)
    someButton.grid(column=0, row=i)

    # Make the button-grid span the entire width
    wn.columnconfigure(i, weight=1)

# Loop to maintain the window
mainloop()