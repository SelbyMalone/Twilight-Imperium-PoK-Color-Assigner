from configparser import ConfigParser
from tkinter import *
from tkinter import messagebox

master = Tk()

factions = []

config = ConfigParser()
config.read('preferences.ini')


class Faction:
    def __init__(self, name, preferences):
        self.name = name
        self.preferences = preferences

    name = ""
    preferences = [int()]
    Color = int(-1)


# records whether a color has been selected yet
colors = ['Red', 'Yellow', 'Green', 'Blue', 'Purple', 'Black', 'Orange', 'Pink']
hexColors = ['#8b0000', '#9b870c', '#006400', '#00008b', '#301934', '#000000', '#ff8c00', '#e75480']
sColors = []

# load factions
file = open("factions.txt")
temp = file.read().splitlines()

for i in temp:
    factions.append(Faction(i, config.get('default', i).split(' ')))
    file.readline()
file.close()
del temp

#button Variables
buttonVars = []
buttons = []


#swap colors
def swapColor(x, y):
    xEnvy = int(factions[x].preferences[factions[y].Color]) - int(factions[x].preferences[factions[x].Color])
    yEnvy = int(factions[y].preferences[factions[x].Color]) - int(factions[y].preferences[factions[y].Color])

    if yEnvy+xEnvy>0:
        factions[x].Color = factions[x].Color ^ factions[y].Color
        factions[y].Color = factions[x].Color ^ factions[y].Color
        factions[x].Color = factions[x].Color ^ factions[y].Color


#assign Faction Color
def assignColor(index):
    best = int(-1)
    bestIndex = int(-1)
    x = 0
    for i in sColors: #for each color check whether it's selected
        #if this color not selected and race prefers this color over their current color
        if i == bool(False) and int(factions[index].preferences[x]) > int(best):
            factions[index].Color = x
            best = factions[index].preferences[x] #record new best preference
            bestIndex = x #records index of best preference
        x+=1
    sColors[bestIndex] = bool(True) #records selected color as selected


def resultsWindow(indexes):
    results = Toplevel()
    T = Text(results,height = len(indexes), width = 50, padx=20, pady=10)
    for i in indexes:
        T.insert(INSERT,str(factions[i].name) + ": " + str(colors[factions[i].Color])+"\n", i)
        T.tag_config(i,foreground=hexColors[factions[i].Color])
    T.pack()
    results.mainloop()


#select button function
def select():
    for i in factions:
        i.Color = int(-1)

    global sColors
    sColors = [bool(0)]*8

    x = 0
    selected = 0
    selectedIndexes = []
    for i in buttonVars:
        if i.get() == 1:
            selected+=1
            if selected > 8:
                messagebox.showerror("Too Many Selections","No more then 8 races can be chosen")
                return
            else:
                selectedIndexes.append(x)
                assignColor(selectedIndexes[selected-1])
        x+=1

    for i in selectedIndexes:
        for j in selectedIndexes:
            if not i == j:
                swapColor(i,j)

    for i in selectedIndexes:
        x = 0
        for j in sColors:
            if j == bool(False) and factions[i].preferences[factions[i].Color] < factions[i].preferences[x]:
                j = bool(False)
                sColors[x] = bool(True)
                factions[i].Color = x
            x+=1

    for i in selectedIndexes:
        print(factions[i].name + " : " + colors[factions[i].Color])

    print("======")

    resultsWindow(selectedIndexes)



# create GUI
master.title("Twilight Imperium Color Assigner")

bRow = 0
bCol = 0
x = 0

for i in factions:
    buttonVars.append(IntVar())
    buttons.append(
        Checkbutton(
            master,
               text=i.name,
               variable=buttonVars[x]).
           grid(row=bRow,
                column=bCol,
                sticky=W))
    bRow += 1
    x += 1
    if bRow > 7:
        bRow = 0
        bCol += 1

Button(
    master,
       text="Select",
       command=select).\
    grid(
        row=9,
        column=0,
        sticky=W,
        padx=10,
        pady=10)

mainloop()