from tkinter import filedialog, ttk
from tkinter import *
from os import getcwd

root = Tk()
root.title('CoG Save Editor')
root.geometry('1250x600')

root.iconbitmap(getcwd() + r"\Assets\cog_logo.ico")

global mysave, others, strings, begin, states, Lines  # test


def initialize():
    global mysave, others, strings, begin, states, Lines

    for x in tabControl.children.values():  # this makes sure that entries and labels from opened saves are not retained =
        if len(x.grid_slaves()) > 0:
            for y in x.grid_slaves():
                y.destroy()

    mysave = filedialog.askopenfile(initialdir=getcwd(), title="Select a save",
                                    filetypes=(("Save File", "*.xml"), ("All files", "*.*")))

    if mysave is None:  # if opening a file is cancelled, removes tabs that were used previously, if any exist
        for x in tabControl.tabs():
            tabControl.hide(x)
        return
    else:
        try:
            tabControl.select(tab_id=".!frame2.!notebook.!frame")  # selects the first tab to be displayed after opening a file
        except TclError:
            None

    Lines = mysave.readlines()
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
            root.title("CoG Save Editor - " + novel.capitalize())  # sets the title of the window to whatever the title of the book is
            begin = line[line.index("{&quot;"):line.index("stats&quot;:{") + len("stats&quot;:{")]  # standard xml line before stat variables appear
            valuesStr = line[line.index("{", line.index("{") + 1) + 1:line.index("sceneName")].replace("&quot;", "\"")  # gets the values of the stats up until "sceneName"

    valuesList = valuesStr.split(",")
    values = {}
    for el in valuesList:
        el = el.replace("\"", "")
        if ":" in el:
            values[el[:el.index(":")]] = el[el.index(":") + 1:]

    entry = 0
    r = 0
    c = 0
    for x, y in values.items():
        if entry < 125 and entry < len(values) + 2:
            var = Label(tab1, text=x.capitalize().replace("_", " ")).grid(row=r, column=c, sticky=W)
            dat = Entry(tab1, width=15)
            dat.insert(0, y)
            dat.grid(row=r, column=c + 1)
            if r % 24 == 0 and r > 0:
                c += 2
                r = 0
            else:
                r += 1
            entry += 1
        if 124 < entry < 250 and entry < len(values) + 2:
            var = Label(tab2, text=x.capitalize().replace("_", " ")).grid(row=r, column=c, sticky=W)
            dat = Entry(tab2, width=15)
            dat.insert(0, y)
            dat.grid(row=r, column=c + 1)
            if r % 24 == 0 and r > 0:
                c += 2
                r = 0
            else:
                r += 1
            entry += 1
        if 249 < entry < 375 and entry < len(values) + 2:
            var = Label(tab3, text=x.capitalize().replace("_", " ")).grid(row=r, column=c, sticky=W)
            dat = Entry(tab3, width=15)
            dat.insert(0, y)
            dat.grid(row=r, column=c + 1)
            if r % 24 == 0 and r > 0:
                c += 2
                r = 0
            else:
                r += 1
            entry += 1
        if 374 < entry < 500 and entry < len(values) + 2:
            var = Label(tab4, text=x.capitalize().replace("_", " ")).grid(row=r, column=c, sticky=W)
            dat = Entry(tab4, width=15)
            dat.insert(0, y)
            dat.grid(row=r, column=c + 1)
            if r % 24 == 0 and r > 0:
                c += 2
                r = 0
            else:
                r += 1
            entry += 1

    if len(tab1.grid_slaves()) > 0:
        tabControl.add(tab1, text="Tab 1")
        tabControl.pack(fill='both', expand=1)
    else:
        try:  # these try and except clauses hide tabs that were previously displayed if they have no grid slaves
            tabControl.hide(tab1)
        except TclError:
            None
    if len(tab2.grid_slaves()) > 0:
        tabControl.add(tab2, text="Tab 2")
        tabControl.pack(fill='both', expand=1)
    else:
        try:
            tabControl.hide(tab2)
        except TclError:
            None
    if len(tab3.grid_slaves()) > 0:
        tabControl.add(tab3, text="Tab 3")
        tabControl.pack(fill='both', expand=1)
    else:
        try:
            tabControl.hide(tab3)
        except TclError:
            None
    if len(tab4.grid_slaves()) > 0:
        tabControl.add(tab4, text="Tab 4")
        tabControl.pack(fill='both', expand=1)
    else:
        try:
            tabControl.hide(tab4)
        except TclError:
            None

    mysave.close()


def getEntries():  # gets a list of the labels and (possibly) modified entries
    entries = []
    for x in tabControl.children.values():
        for y in reversed(x.grid_slaves()):
            if type(y) == Entry:
                entries.append(y.get())
            else:
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
    rejoin(e)

    for l in Lines:  # finds which line is the current state of the novel (i.e. not the temp or backup states)
        if "PSstate\">" in l:
            ind = Lines.index(l)

    scenename = Lines[ind][Lines[ind].index(",&quot;sceneName"):]
    # print(scenename)
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
frame2.pack(fill="both")
tabControl = ttk.Notebook(frame2)

# create necessary tabs
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)
tab5 = ttk.Frame(tabControl)

root.mainloop()
