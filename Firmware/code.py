#Running Adafruit CircuitPython 6.3.0 on 2021-06-01
import board
import busio
import displayio
import terminalio #Just a font
import adafruit_ili9341
from adafruit_display_text import label
import adafruit_imageload
import time
from adafruit_display_shapes.line import Line
from adafruit_bitmap_font import bitmap_font
import rotaryio
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

#custom lib
from keys_dict.keys import key_lookup


#Functions -----------------------
#get milli second
def millis():
    return int(round(time.time() * 1000))

# Make grid with line
def draw_grid_lines():
    #Standing line
    col_line_1 = Line(105,0,105,240,color=0xFFFFFF)
    splash.append(col_line_1)
    col_line_2 = Line(210,0,210,240,color=0xFFFFFF)
    splash.append(col_line_2)

    #Sleeping line
    row_line_1 = Line(0,60,320,60,color=0xFFFFFF)
    splash.append(row_line_1)

    row_line_2 = Line(0,120,320,120,color=0xFFFFFF)
    splash.append(row_line_2)

    row_line_3 = Line(0,180,320,180,color=0xFFFFFF)
    splash.append(row_line_3)

#print shortcuts of that application
def print_shortcuts(application_id):
    print("----------------")
    i=1
    with open("/shortcuts.txt","r") as fp:
        print(application_id)
        for line in fp:
            app,desc,keys = line.split(",")
            if app == application_id:
                print(i,desc,keys,end='')
                #key_1_area.text = desc   #Update label
                if i%3 ==0 :
                    print()
                i=i+1
#print_shortcuts('Zoom')
def draw_display(application_id):
    print("----------------")
    print(application_id)
    i=0
    with open("/shortcuts.txt","r") as fp:
        for line in fp:
            app,desc,keys = line.split(",")
            if app == application_id:
                #print(i,desc,keys,end='')
                key_text[i] = desc
                i=i+1
    app_area.text = application_id
    key_1_area.text = key_text[0]
    key_2_area.text = key_text[1]
    key_3_area.text = key_text[2]
    key_4_area.text = key_text[3]
    key_5_area.text = key_text[4]
    key_6_area.text = key_text[5]
    key_7_area.text = key_text[6]
    key_8_area.text = key_text[7]
    key_9_area.text = key_text[8]
    key_10_area.text = key_text[9]
    key_11_area.text = key_text[10]
    key_12_area.text = key_text[11]
    print(key_text)

# Functions ends -----------------


#Display init
#----------------------

displayio.release_displays()

dc=board.GP22
rst=board.GP26
blk=board.GP28
cs=board.GP21 #My display does not have it...

spi = busio.SPI(clock=board.GP18, MOSI=board.GP19, MISO=board.GP20)

displayio.release_displays()
display_bus = displayio.FourWire(spi, command = dc, chip_select=cs, reset=rst)


display = adafruit_ili9341.ILI9341(display_bus, width=320, height=240)
splash = displayio.Group(max_size=10)
display.show(splash)

#Rotary encoder
encoder = rotaryio.IncrementalEncoder(board.GP16, board.GP17)
last_position = encoder.position
#cc = ConsumerControl(usb_hid.devices)
button_state = None
button = digitalio.DigitalInOut(board.GP14)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP


#keypad
keypress_pins = [board.GP0,
                board.GP1,
                board.GP2,
                board.GP3,
                board.GP4,
                board.GP5,
                board.GP6,
                board.GP7,
                board.GP8,
                board.GP9,
                board.GP10,
                board.GP11]

key_pin_array = []

application_id_array=[]
key_codes = []
keys_press = []

keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)
debounce_time = 100

#pull up all pins
for pin in keypress_pins:
    key_pin = digitalio.DigitalInOut(pin)
    key_pin.direction = digitalio.Direction.INPUT
    key_pin.pull = digitalio.Pull.UP
    key_pin_array.append(key_pin)
#Read Shortcuts file
application_dict={}

with open("/shortcuts.txt","r") as fp:
    for line in fp:
        app,desc,keys = line.split(",")
        combo=[]
        for key in keys.split():
            combo.append(key_lookup[key])

        if app in application_dict:
            application_dict[app].append((desc.strip(),combo))
        else:
            application_dict[app] = [(desc.strip(),combo)]


#if desktop is a set of shortcuts in the file then start with that as the default

#sort dict alphabetically
# sorted_dict = dict(sorted(app_dict.items()))

if "Desktop" in application_dict.keys():
    application_id = "Desktop"
else:
    application_id = list(application_dict.keys())[0]

##Labels

#TODO make this into function adn in loop

key_text = []
for i in range (0,12):
    key_text.append("Default")

font_color = 0xFFFFFF
app_label_group = displayio.Group(max_size=10, scale=1, x=5, y=10)
app_text = "Default"
app_area = label.Label(terminalio.FONT, text=app_text, color=font_color)
app_label_group.append(app_area)
splash.append(app_label_group)
#--------------
key_1_label_group = displayio.Group(max_size=10, scale=1, x=10, y=20)
key_1_text = "Default"
key_1_area = label.Label(terminalio.FONT, text=key_1_text, color=font_color)
key_1_label_group.append(key_1_area)
splash.append(key_1_label_group)

key_2_label_group = displayio.Group(max_size=10, scale=1, x=125, y=20)
key_2_text = "Default"
key_2_area = label.Label(terminalio.FONT, text=key_2_text, color=font_color)
key_2_label_group.append(key_2_area)
splash.append(key_2_label_group)

key_3_label_group = displayio.Group(max_size=10, scale=1, x=230, y=20)
key_3_text = "Default"
key_3_area = label.Label(terminalio.FONT, text=key_3_text, color=font_color)
key_3_label_group.append(key_3_area)
splash.append(key_3_label_group)
#--------------------------------------
key_4_label_group = displayio.Group(max_size=10, scale=1, x=10, y=80)
key_4_text = "Default"
key_4_area = label.Label(terminalio.FONT, text=key_4_text, color=font_color)
key_4_label_group.append(key_4_area)
splash.append(key_4_label_group)

key_5_label_group = displayio.Group(max_size=10, scale=1, x=125, y=80)
key_5_text = "Default"
key_5_area = label.Label(terminalio.FONT, text=key_5_text, color=font_color)
key_5_label_group.append(key_5_area)
splash.append(key_5_label_group)

key_6_label_group = displayio.Group(max_size=10, scale=1, x=230, y=80)
key_6_text = "Default"
key_6_area = label.Label(terminalio.FONT, text=key_6_text, color=font_color)
key_6_label_group.append(key_6_area)
splash.append(key_6_label_group)
#-----------------------------------------
key_7_label_group = displayio.Group(max_size=10, scale=1, x=10, y=140)
key_7_text = "Default"
key_7_area = label.Label(terminalio.FONT, text=key_7_text, color=font_color)
key_7_label_group.append(key_7_area)
splash.append(key_7_label_group)

key_8_label_group = displayio.Group(max_size=10, scale=1, x=125, y=140)
key_8_text = "Default"
key_8_area = label.Label(terminalio.FONT, text=key_8_text, color=font_color)
key_8_label_group.append(key_8_area)
splash.append(key_8_label_group)

key_9_label_group = displayio.Group(max_size=10, scale=1, x=230, y=140)
key_9_text = "Default"
key_9_area = label.Label(terminalio.FONT, text=key_9_text, color=font_color)
key_9_label_group.append(key_9_area)
splash.append(key_9_label_group)
#-----------------------------------------
key_10_label_group = displayio.Group(max_size=10, scale=1, x=10, y=200)
key_10_text = "Default"
key_10_area = label.Label(terminalio.FONT, text=key_10_text, color=font_color)
key_10_label_group.append(key_10_area)
splash.append(key_10_label_group)

key_11_label_group = displayio.Group(max_size=10, scale=1, x=125, y=200)
key_11_text = "Default"
key_11_area = label.Label(terminalio.FONT, text=key_11_text, color=font_color)
key_11_label_group.append(key_11_area)
splash.append(key_11_label_group)

key_12_label_group = displayio.Group(max_size=10, scale=1, x=230, y=200)
key_12_text = "Default"
key_12_area = label.Label(terminalio.FONT, text=key_12_text, color=font_color)
key_12_label_group.append(key_12_area)
splash.append(key_12_label_group)
#-----------------------------------------


#-----------------------
draw_grid_lines()
current_pressed_key=12

#---Main loop
while True:
    #Check rotary movement
    current_position = encoder.position
    position_change = current_position - last_position
    if position_change > 0:
        for _ in range(position_change):
            idx = list(application_dict.keys()).index(application_id)
            application_id = list(application_dict.keys())[(idx+1)%len(list(application_dict.keys()))]
            #print shortcuts of that application
            #print_shortcuts(application_id)
            draw_display(application_id)
    elif position_change < 0:
        for _ in range(-position_change):
            idx = list(application_dict.keys()).index(application_id)
            application_id = list(application_dict.keys())[(idx-1)%len(list(application_dict.keys()))]
            #print_shortcuts(application_id)
            draw_display(application_id)
    last_position = current_position

    #detect keypresses
    for key_pin in key_pin_array:
        if not key_pin.value:
            i = key_pin_array.index(key_pin)
            
            if (current_pressed_key is not i):
                current_time = millis()

            while key_pin.value:
                pass
                #on key press release continue to look up shortcut keypress required and press it.
            key = application_dict[application_id][i][1]
            #if (current_pressed_key != i) or (millis() - current_time > debounce_time):
            #if (current_pressed_key is not i) or millis() - current_time > debounce_time:
            if (current_pressed_key is not i) or millis() - current_time > debounce_time:
                keyboard.press(*key)
                keyboard.release_all()
                current_pressed_key = i
    time.sleep(0.1)



#--------------------
#Load font
# try uncommenting different font files if you like
#font_file = "fonts/LeagueSpartan-Bold-16.bdf"
#font_file = "fonts/Junction-regular-24.bdf"

#font = bitmap_font.load_font(font_file)

#---------

# Draw a label
# text_group = displayio.Group(max_size=10, scale=1, x=57, y=120)
# text = "Hello World!"
# text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00)
# text_group.append(text_area)  # Subgroup for text scaling
# splash.append(text_group)



#Make Labels with terminalio font
# text_group = displayio.Group(max_size=10, scale=1, x=20, y=20)
# text = "Hello World!"
# text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00)
# text_group.append(text_area)  # Subgroup for text scaling
# splash.append(text_group)

#Make Labels with bitmap font
# text = "HELLO WORLD"
# color = 0xFF00FF

# # Create the text label
# text_area = label.Label(font, text=text, color=color)

# # Set the location
# text_area.x = 20
# text_area.y = 20

# # Show it
# #display.show(text_area)
# splash.append(text_area)

#Biitmap font end----


#Make Labels with terminalio font
# text_group = displayio.Group(max_size=10, scale=1, x=20, y=20)
# text = "Hello World!"
# text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00)
# text_group.append(text_area)  # Subgroup for text scaling
# splash.append(text_group)


# text = "Hello world"
# text_area = label.Label(terminalio.FONT, text=text)
# text_area.x = 10
# text_area.y = 10
# board.DISPLAY.show(text_area)j