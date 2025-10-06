import time
import board
import busio
import digitalio
import usb_hid
import json
from adafruit_mcp230xx.MCP23017 import MCP23017
from adafruit_hid.keyboard import Keyboard

i2c = busio.I2C(board.GP1, board.GP0)
kbd = Keyboard(usb_hid.devices)


mcp = MCP23017(i2c,address=0x20)


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
layer = 0
keyDown = []
keyUp = []





#Assign inputs and outputs, note the Pull.UP
for r in row:
    r.direction = digitalio.Direction.OUTPUT

for idc, c in enumerate(col):
    c.direction = digitalio.Direction.INPUT
    c.pull = digitalio.Pull.UP

with open('keyBind.json', 'r') as file:
    layers = json.load(file)["layers"]
    
#Maps the keycodes to positions in the grid
keyMap = []
#Fill in map with nulls
for l in layers:
    mapLayer = []
    for r in l:
        mapRow = []
        for c in r:
            mapRow.append(None)
        mapLayer.append(mapRow)
    keyMap.append(mapLayer)
        

with open('keyBind.json', 'r') as file:
    layers = json.load(file)["layers"]

for idl, bindingLayer in enumerate(layers):
    for idr, bindingRows in enumerate(bindingLayer):
        #map.append([])
        #mapRow = []
        for idc, bindingCols in enumerate(bindingRows):
            binding = bindingLayer[idr][idc]
            keyMap[idl][idr][idc] = []
            
            if "modifier" in binding:
                if binding["modifier"] == "altGr":
                    keyMap[idr][idc].append(0xE6)
                if binding["modifier"] == "alt":
                    keyMap[idr][idc].append(0xE2)
                if binding["modifier"] == "ctrl":
                    keyMap[idr][idc].append(0xE0)
                if binding["modifier"] == "shift":
                    keyMap[idr][idc].append(0xE1)
            
            
            hidNumber = binding["hid"];
            keyMap[idl][idr][idc].append(hidNumber)


print(keyMap)
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
                for key in keyMap[layer][idr][idc]:
                    if not key is None:
                        pressedKeys.append(key)
                    
    #Get which keys got pressed since last loop and which was released
    keyDown= list(set(pressedKeys) - set(previouslyPressedKeys))
    keyUp= list(set(previouslyPressedKeys) - set(pressedKeys))
    print(keyDown)
    kbd.press(*keyDown)
    kbd.release(*keyUp)
    previouslyPressedKeys = pressedKeys


