import time
import serial.tools.list_ports
from CodeePy import CodeePy

# get current COM PORTS  #Maybe useful in interface creation
CodeePy.get_com_ports()

# create CodeePy Instance and open connection
# Insert your COM port here <'COM13'>
#board = CodeePy('COM13')

# say text
#board.say("Hello")

# set melody tempo
#board.set_melody_tempo(2)

# play melody
#board.play_melody("little lamb")

# play tone
#board.play_tone(2000, 300)

# play notes fixed duration
#board.play_notes(["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"], 1)  #C Major Scale
#board.exit()

#board.play_notes_with_duration(["C4.1", "D4.3", "E4.1", "F4.2", "G4.1", "A4.3", "B4.1", "C5.1"])
#board.exit()

#set left arm 30 degrees
#board.set_left_arm(30)

#Swing both arms for 5 seconds then stop
# set arms to on
#board.swing_arms(2, True)
# set delay
#time.sleep(5)
# stop arms
#board.stop_arms()
#board.exit()

# test look around
# set look around to on
# board.look_around(2, True)
# set delay
#time.sleep(3)
# stop look around
#board.stop_look_around()

#Set head image
# board.display_image("tick")

#Text scroll
#board.led_scroll_text("abcde")

#Display number
#board.display_number(85)

#Clear Display
#board.display_clear()

#Set LED display pixel state
#board.set_led_display_pixel(0, 0, True)

#Changebluetooth name
#board.change_bot_bluetooth_name("Grumpee")

#Run single line sensor id no 5 for 4 seconds
#board.read_line_sensor(5,4)

#Get darkest position under all 5 line sensors
#print(board.read_line_position(5))

#Test Codee's wheel servos
#for x in range(10):
#    board.set_left_wheel_velocity(10)
#    board.set_right_wheel_velocity(10)
#    time.sleep(0.25)
#board.set_left_wheel_velocity(0)
#board.set_right_wheel_velocity(0)

#Reset Codee to default
#board.reset_codee_body_and_exit()

