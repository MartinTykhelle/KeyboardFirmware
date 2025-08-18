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
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
import storage

i2c = busio.I2C(board.GP1, board.GP0)
mcp = []



num_rows = 5
num_columns = 8
specialBoot = False
found_modules = []
row_masks = [0b11111110, 0b11111101, 0b11111011, 0b11110111, 0b11101111]

kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)

i2c.try_lock()
#Scan I2c and add devices
for address in i2c.scan(): 
    found_modules.append(address)
i2c.unlock()

#When i2c is unlocked, add the modules
for address in found_modules:
    mcp.append(MCP23017(i2c,address=address))

#Set up each mcp chip
for module in mcp:
    #enable pull up on GPA
    module.gppua = 0b11111111
    #Set pin direction on GPA to input
    module.iodira = 0b11111111
    #Set pin direction on GPB to output
    module.iodirb = 0b00000000

#Add up the new total columns
total_num_columns = num_columns*len(mcp)
#Set up mapping
keyMap = []

    

with open('bindings.json', 'r') as file:
    bindings = json.load(file)["bindings"]
    
#Fill in map with Nones
for idr, bindingRows in enumerate(bindings):
    mapRow = []
    for idc, bindingCols in enumerate(bindingRows):
        mapRow.append(None)
    keyMap.append(mapRow)

for idr, bindingRows in enumerate(bindings):

    for idc, bindingCols in enumerate(bindingRows):
        binding = bindings[idr][idc]
        keyMap[idr][idc] = []
        
        
        if "modifier" in binding:
            if binding["modifier"] == "C":
                keyMap[idr][idc].append(keyCodes["LEFT_CONTROL"])
            if binding["modifier"] == "S":
                keyMap[idr][idc].append(keyCodes["LEFT_SHIFT"])

        keyMap[idr][idc].append(keyCodes[binding["keyCode"]])


cols = [0]*len(row_masks)
prevCols = [0]*len(row_masks)
initialized = False
#Failsafe in case it reboots without with keys held down
kbd.release_all()

#Check if the top-left button is pressed on boot
mcp[0].gpiob = row_masks[0]
specialBoot = mcp[0].gpioa == 0b11111110

rotaryA = digitalio.DigitalInOut(board.GP2)
rotaryB = digitalio.DigitalInOut(board.GP3)
rotaryButton = digitalio.DigitalInOut(board.GP4)

rotaryA.pull = digitalio.Pull.UP
rotaryB.pull = digitalio.Pull.UP
rotaryButton.pull = digitalio.Pull.UP
volume = [0,0,0,0,0]
rotaryButtonState = rotaryButton.value

while True:
    for idr, row in enumerate(row_masks):
        col = 0
        for idm, module in enumerate(mcp):
            module.gpiob = row
            #"concatenates" binary numbers
            col += module.gpioa<<8*(idm)
        cols[idr] = col

    #Do bitwise magic on read state, needs to be fast
    pressed_buttons = []
    released_buttons = []
    for idr in range(len(cols)):
        state = cols[idr]
        prev_state = prevCols[idr]
        
        #Checks if a button has been pressed on released
        pressed =  (state ^ prev_state)&~state
        released = (state ^ prev_state)&state
        #print(pressed)
        
        #Not sure how this can be improved
        if initialized:
            for pos in range(8*len(mcp)):
                if pressed & (1<<pos) > 0:
                    for key in keyMap[idr][pos]:
                        pressed_buttons.append(key)
                if released & (1 << pos) > 0:
                    for key in keyMap[idr][pos]:
                        released_buttons.append(key)
                
        prevCols[idr] = cols[idr]
        
    initialized = True
    #print(pressed_buttons, released_buttons)
    
    #time.sleep(1)
    #print(specialBoot)
    #print(rotaryA.value, rotaryB.value)
    volChange = 0
    if rotaryA.value and not rotaryB.value:
        volChange = -1 
    if not rotaryA.value and rotaryB.value:
        volChange = 1
    
    volume.pop(0)
    volume.append(volChange)
    #print(volume)
    if(sum(volume) >1):
        cc.press(ConsumerControlCode.VOLUME_INCREMENT)
        time.sleep(0.01)
        cc.release()
        volume = [0,0,0,0,0]
    if(sum(volume) <-1):
        cc.press(ConsumerControlCode.VOLUME_DECREMENT)
        time.sleep(0.01)
        cc.release()
        volume = [0,0,0,0,0]
    if rotaryButtonState != rotaryButton.value and not rotaryButton.value:
        cc.press(ConsumerControlCode.PLAY_PAUSE)
    rotaryButtonState = rotaryButton.value
    kbd.press(*pressed_buttons)
    kbd.release(*released_buttons)


