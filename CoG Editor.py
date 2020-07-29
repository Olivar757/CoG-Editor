from math import ceil
from os import getcwd
from tkinter import *
from tkinter import filedialog, ttk

root = Tk()
root.title('CoG Save Editor')
root.geometry('1250x600')

root.iconbitmap(getcwd() + r"\Assets\cog_logo.ico")

global mySave, others, strings, begin, states, Lines


def populate(tab, iteration, lim, values):
    r, c = 0, 0
    for x, y in values.items():
        if iteration == lim:
            tab += 1
            lim += 125
        var = Label(tabControl.winfo_children()[tab], text=x.capitalize().replace("_", " ")).grid(row=r, column=c,
                                                                                                  sticky=W)
        dat = Entry(tabControl.winfo_children()[tab], width=15)
        dat.insert(0, y)
        dat.grid(row=r, column=c + 1)
        if r % 24 == 0 and r > 0:
            c += 2
            r = 0
        else:
            r += 1
        iteration += 1
    tabControl.pack(fill=BOTH, expand=1)


def initialize():
    global mySave, others, strings, begin, states, Lines

    for x in tabControl.winfo_children():  # this makes sure that entries, labels, and tabs from opened saves are not retained
        if len(x.grid_slaves()) > 0:
            for y in x.grid_slaves():
                y.destroy()
        x.destroy()

    mySave = filedialog.askopenfile(initialdir=getcwd(), title="Select a save",
                                    filetypes=(("Save File", "*.xml"), ("All files", "*.*")))

    if mySave is None:  # if opening a file is cancelled, removes tabs that were used previously, if any exist
        for x in tabControl.tabs():
            tabControl.hide(x)
        return
    else:
        try:
            tabControl.select(tab_id=".!frame2.!notebook.!frame")  # selects the first tab to be displayed after opening a file
        except TclError:
            pass

    Lines = mySave.readlines()
    others = []
    strings = []
    states = []

    for line in Lines:  # gets essential lines and lines with actual data
        if "PSstate" in line:
            strings.append(line)
            states.append(line[:line.index(">{") + 1])
        else:
            others.append(line)

    for line in strings:
        if "PSstate\"" in line:
            novel = line[20:]
            novel = novel[:novel.index("PSstate")]
            root.title(
                "CoG Save Editor - " + novel.capitalize())  # sets the title of the window to whatever the title of the book is
            begin = line[line.index("{&quot;"):line.index("stats&quot;:{") + len(
                "stats&quot;:{")]  # standard xml line before stat variables appear
            valuesStr = line[line.index("{", line.index("{") + 1) + 1:line.index("</string>")].replace("&quot;",
                                                                                                       "\"")  # gets the values of the stats

    valuesList = valuesStr.split(",")
    values = {}
    for el in valuesList:
        el = el.replace("\"", "")
        if ":" in el:
            values[el[:el.index(":")]] = el[el.index(":") + 1:]

    for t in range(ceil(len(values) / 125)):
        tab = ttk.Frame(tabControl)
        t += 1
        tabControl.add(tab, text="Tab %d" % t)

    populate(0, 0, 125, values)
    mySave.close()


def getEntries():  # gets a list of the labels and (possibly) modified entries
    entries = []
    for x in tabControl.children.values():
        for y in reversed(x.grid_slaves()):
            if type(y) == Entry:
                entries.append(y.get())
            else:
                if y.cget(key='text') == "Scenename":
                    entries.append("sceneName")
                    continue
                entries.append(y.cget(key="text").lower().replace(" ", "_"))
    return entries


def rejoin(e):  # takes in the list of entries and rejoins the entries and labels into what it originally looked like in the settings.xml file
    for x in range(len(e) // 2):
        if e[x + 1] == "false" or e[x + 1] == "true" or e[x + 1].isdigit():
            e[x] = "&quot;" + e[x] + "&quot;:" + e[x + 1] + ","
        else:
            e[x] = "&quot;" + e[x] + "&quot;:&quot;" + e[x + 1] + "&quot;,"
        e.pop(x + 1)
    return e


def save():
    global others, strings, begin, Lines

    e = getEntries()
    print(type(e))
    print(e)
    rejoin(e)

    for l in Lines:  # finds which line is the current state of the novel (i.e. not the temp or backup states)
        if "PSstate\">" in l:
            ind = Lines.index(l)

    scenename = Lines[ind][Lines[ind].index(",&quot;temps&quot;"):]
    changed = begin + "".join(e)[:-1] + scenename

    f = filedialog.asksaveasfile(filetypes=(("XML File", "*.xml"), ("All Files", "*.*")), mode="w+")

    for x in states:
        states[states.index(x)] = x + changed + "\r"

    Lines[ind] = Lines[ind][:Lines[ind].index("{&q")] + changed
    if f is None:
        return
    else:
        f.writelines(Lines)
        f.close()


# Creating buttons
frame = Frame(root, padx=10)
openBtn = Button(frame, text="Open file", command=initialize).grid(row=0, column=0)
saveBtn = Button(frame, text="Save File", command=save).grid(row=0, column=1, pady=10, padx=10)
frame.pack(padx=10)

# Creating tabControl
frame2 = Frame(root)
frame2.pack(fill="both", expand=True)
tabControl = ttk.Notebook(frame2)

root.mainloop()
