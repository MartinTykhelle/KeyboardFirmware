import time
import board
import busio
import digitalio
import usb_hid
import json
from keycode import keyCodes
from adafruit_mcp230xx.MCP23017 import MCP23017
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

i2c = busio.I2C(board.GP1, board.GP0)
kbd = Keyboard(usb_hid.devices)


mcp = MCP23017(i2c,address=0x21)


row = []
col = []
#Assign pins to rows and columns
row.append(mcp.get_pin(8))
row.append(mcp.get_pin(9))
row.append(mcp.get_pin(10))
row.append(mcp.get_pin(11))
row.append(mcp.get_pin(12))
col.append(mcp.get_pin(0))
col.append(mcp.get_pin(1))
col.append(mcp.get_pin(2))
col.append(mcp.get_pin(3))
col.append(mcp.get_pin(4))
col.append(mcp.get_pin(5))
col.append(mcp.get_pin(6))
col.append(mcp.get_pin(7))

pressedKeys = []
previouslyPressedKeys = []
keyDown = []
keyUp = []





#Assign inputs and outputs, note the Pull.UP
for r in row:
    r.direction = digitalio.Direction.OUTPUT

for idc, c in enumerate(col):
    c.direction = digitalio.Direction.INPUT
    c.pull = digitalio.Pull.UP


#Maps the keycodes to positions in the grid
keyMap = []
#Fill in map with nulls
for r in row:
    mapRow = []
    for c in col:
        mapRow.append(None)
    keyMap.append(mapRow)


with open('bindings.json', 'r') as file:
    bindings = json.load(file)["bindings"]

for idr, bindingRows in enumerate(bindings):
    #map.append([])
    #mapRow = []
    for idc, bindingCols in enumerate(bindingRows):
        binding = bindings[idr][idc]
        keyMap[idr][idc] = []

        if "modifier" in binding:
            if binding["modifier"] == "C":
                keyMap[idr][idc].append(keyCodes["LEFT_CONTROL"])
            if binding["modifier"] == "S":
                keyMap[idr][idc].append(keyCodes["LEFT_SHIFT"])

        keyMap[idr][idc].append(keyCodes[binding["keyCode"]])
        #print(idr, idc, bindings[idr][idc])



while True:

    pressedKeys = []
    #Sweep rows
    for idr, currentRow in enumerate(row):
	    #Set the other rows to HIGH
        for r in row:
            r.value = True
        #Set this row to LOW
        currentRow.value = False
        for idc, currentCol in enumerate(col):
	        #If the key is pressed it is LOW, the others are HIGH
            if not currentCol.value:
                for key in keyMap[idr][idc]:
                    pressedKeys.append(key)
    #Get which keys got pressed since last loop and which was released
    keyDown= list(set(pressedKeys) - set(previouslyPressedKeys))
    keyUp= list(set(previouslyPressedKeys) - set(pressedKeys))
    kbd.press(*keyDown)
    kbd.release(*keyUp)
    previouslyPressedKeys = pressedKeys


