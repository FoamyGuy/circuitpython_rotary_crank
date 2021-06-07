import board
import digitalio
import rotaryio
import usb_hid
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.mouse import Mouse

mouse = Mouse(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)

encoder = rotaryio.IncrementalEncoder(board.ROTA, board.ROTB)
switch = digitalio.DigitalInOut(board.SWITCH)
switch.switch_to_input(pull=digitalio.Pull.DOWN)

switch_state = None
last_position = encoder.position

MODE_BRIGHTNESS = 0
MODE_SCROLL = 1

MODE = MODE_BRIGHTNESS

while True:
    current_position = encoder.position
    position_change = current_position - last_position
    if position_change > 0:
        for _ in range(position_change):

            print(position_change)
            if MODE == MODE_BRIGHTNESS:
                cc.send(ConsumerControlCode.BRIGHTNESS_INCREMENT)
            if MODE == MODE_SCROLL:
                mouse.move(wheel=1)
        print(current_position)
    elif position_change < 0:
        for _ in range(-position_change):
            print(position_change)
            if MODE == MODE_BRIGHTNESS:
                cc.send(ConsumerControlCode.BRIGHTNESS_DECREMENT)
            if MODE == MODE_SCROLL:
                mouse.move(wheel=-1)
        print(current_position)
    last_position = current_position
    if not switch.value and switch_state is None:
        switch_state = "pressed"
    if switch.value and switch_state == "pressed":
        print("switch pressed.")
        if MODE == MODE_SCROLL:
            MODE = MODE_BRIGHTNESS
        else:
            MODE = MODE_SCROLL
        switch_state = None