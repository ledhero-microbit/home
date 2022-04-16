from microbit import *
import music
import time
import random


# CONFIGURABLE VARIABLES

notesCollection = [
    "C4:2", "C4:2", "G4:2", "G4:2", "A4:2", "A4:2", "G4:7",
    "F:2", "F:2", "E4:2", "E4:2", "D4:2", "D4:2", "C4:7",
    "G4:2", "G4:2", "F4:2", "F4:2", "E4:2", "E4:2", "D4:7",
    "G4:2", "G4:2", "F4:2", "F4:2", "E4:2", "E4:2", "D4:7",
    "C4:2", "C4:2", "G4:2", "G4:2", "A4:2", "A4:2", "G4:7",
    "F:2", "F:2", "E4:2", "E4:2", "D4:2", "D4:2", "C4:7"
]

on = "4"
off = "0"
lateralOfRow = "1"
successLightBrightness = "9"
failureLightBrightness = "2"
failureNote = "C2:2"
presetSleepTimeToReact = 0.3
presetDelayValue = 100


# NO-CONFIGURABLE VARIABLES

actualNote, counter, hitsCounter = 0, 0, 0
correctButtonHasPressed = False
startingAnimationFrames, endAnimationFrame, leftLight, middleLight, rightLight, rowOff, rowOn = str, str, str, str, str, str, str


# METHODS

def selectRandomLight():
    global leftLight, middleLight, rightLight

    randomLight = random.randint(1, 3)
    if randomLight == 1:
        leftLight, middleLight, rightLight = on, off, off
    elif randomLight == 2:
        leftLight, middleLight, rightLight = off, on, off
    else:
        leftLight, middleLight, rightLight = off, off, on

def createTheDescentAnimationOfSelectedLight():
    global startingAnimationFrames, rowOff, rowOn

    rowOff = lateralOfRow + off + off + off + lateralOfRow + ":"
    rowOn = lateralOfRow + leftLight + middleLight + rightLight + lateralOfRow + ":"

    frame01 = Image(rowOn + rowOff * 4)
    frame02 = Image(rowOff + rowOn + rowOff * 3)
    frame03 = Image(rowOff * 2 + rowOn + rowOff * 2)
    frame04 = Image(rowOff * 3 + rowOn + rowOff)
    startingAnimationFrames = [frame01, frame02, frame03, frame04]

def checkIfTheCorrectButtonHasBeenPressed():
    global correctButtonHasPressed

    time.sleep(presetSleepTimeToReact)

    if leftLight != off:
        if button_a.is_pressed():
            correctButtonHasPressed = True
        else:
            correctButtonHasPressed = False
    elif middleLight != off:
        if button_a.is_pressed() and button_b.is_pressed():
            correctButtonHasPressed = True
        else:
            correctButtonHasPressed = False
    else:
        if button_b.is_pressed():
            correctButtonHasPressed = True
        else:
            correctButtonHasPressed = False

def changeActualNoteToFailureNote():
    global notesCollection
    notesCollection[actualNote] = failureNote

def modifyTheSelectedLightBrightness():
    global leftLight, middleLight, rightLight

    if correctButtonHasPressed:
        if leftLight != off:
            leftLight = successLightBrightness
        elif middleLight != off:
            middleLight = successLightBrightness
        else:
            rightLight = successLightBrightness
    else:
        if leftLight != off:
            leftLight = failureLightBrightness
        elif middleLight != off:
            middleLight = failureLightBrightness
        else:
            rightLight = failureLightBrightness

def createEndAnimationFrame():
    global rowOn, endAnimationFrame

    rowOn = lateralOfRow + leftLight + middleLight + rightLight + lateralOfRow + ":"

    endAnimationFrame = Image(rowOff * 4 + rowOn)

def playActualNote():
    global actualNote

    if actualNote < len(notesCollection):
        music.play(notesCollection[actualNote])
        actualNote += 1

def refreshHitCounter():
    global hitsCounter
    if correctButtonHasPressed:
        hitsCounter += 1


# GAME LOOP
while counter < len(notesCollection):
    selectRandomLight()
    createTheDescentAnimationOfSelectedLight()

    display.show(startingAnimationFrames, delay=presetDelayValue)

    checkIfTheCorrectButtonHasBeenPressed()
    if not correctButtonHasPressed:
      changeActualNoteToFailureNote()
    modifyTheSelectedLightBrightness()
    createEndAnimationFrame()

    display.show(endAnimationFrame)

    playActualNote()

    refreshHitCounter()
    counter += 1
    
    
# SCORE
display.scroll("HITS: " + str(hitsCounter))
