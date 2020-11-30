# CoG-Editor
Editor for use on settings.xml files generated from games from the publisher Choice of Games LLC.

I've always wanted save editor for novels published by Choice of Games LLC, and quarantine gave me the opportunity to try and make one. This is the app in its simplest version since I've never created a desktop application before.
If you find any bugs or something doesn't work, email me at COGeditor20@gmail.com, and I'll try and figure out a solution.

Working with the following novels:
  - Silverworld
  - Werewolves: Haven Rising

## How to use the editor
*Note: This tutorial is assuming you are using BluestacksTweaker, however the instructions are likely similar for whatever emulator/tool you are using.

In the bluestacks tweaker interface, locate and open (if necessary) the File Manager.  
 - On the right side of this tab, there's a file explorer that is the storage of the phone being emulated.  
 - On the left, the file explorer shown is one for your computer.  
 
To find the folders for each game, navigate to the "/data/data/" directory in the phone's file explorer. This directory contains the data for different apps, we are interested in games from Choice of Games LLC and Hosted Games, which would be in a folder that looks something like this:

For games published by Choice of Games LLC:
```shell
"com.choiceofgames.______"    (the underlined portion would be the name of the game)
```
For games published by Hosted Games:
 ```shell
"org.hostedgames.______"    (the underlined portion would be the name of the game)
```

Navigate to the shared_prefs folder and find the settings.xml file. Copy this file to your computer's storage.  
**Before editing your settings.xml file, I'd highly recommend making a backup in case the editor doesn't work.**  
This is the file that you upload into the save editor. Once you save the file after editing, you replace the file in the com.choiceofgames.\_\_\_\_\_\_ directory in the emulated phone.
