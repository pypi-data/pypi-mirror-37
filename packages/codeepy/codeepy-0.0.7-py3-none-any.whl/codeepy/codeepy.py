"""
LICENSE:
===============

    Copyright (c) 2018 Marita Fitzgerald and the Creative Science Foundation. All rights reserved.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

QUICK TUTORIAL:
===============

## view CodeePy Documentation
help(CodeePy)

# get current COM PORTS
CodeePy.get_com_ports()

# create CodeePy Instance and open connection
board = CodeePy('<Your COM Port>')

# say text
board.say("Hello")

# set melody tempo & play melody
board.set_melody_tempo(2)
board.play_melody("little lamb")

# play tone
board.play_tone(2000, 300)

# play notes fixed duration
board.play_notes(["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"], 1)  #C Major Scale
board.exit()

#play notes with variable duration
board.play_notes_with_duration(["C4.1", "D4.3", "E4.1", "F4.2", "G4.1", "A4.3", "B4.1", "C5.1"])
board.exit()

#set left arm 30 degrees
board.set_left_arm(30)
board.exit()

#Swing both arms for 5 seconds then stop
#set arms to on
board.swing_arms(2, True)
#set delay
time.sleep(5)
#stop arms
board.stop_arms()
board.exit()

#Set degrees of both arms
#board.set_arms(0, 0)

#Look around
# set look around to on
board.look_around(2, True)
#set delay
time.sleep(3)
#stop look around
board.stop_look_around()
board.exit()

#Set head image
board.display_image("tick")

#Text scroll
board.led_scroll_text("abcde")

#Display number
board.display_number(85)

#Clear Display
board.display_clear()

#Set LED display pixel state
board.set_led_display_pixel(0, 0, True)

#Changebluetooth name
board.change_bot_bluetooth_name("happybot")

#Run single line sensor id no 5 for 4 seconds
#board.read_line_sensor(5,4)

#returns an array of all the sensor values that detect a black line, 1 is true 0 is false
#You can all 5 or inner 3 sensors as int
print(board.read_line_position(5))

#Test Codee's wheel servos
for x in range(10):
    board.set_left_wheel_velocity(10)
    board.set_right_wheel_velocity(10)
    time.sleep(0.25)
board.set_left_wheel_velocity(0)
board.set_right_wheel_velocity(0)

#Set both wheel speeds
#board.set_wheel_velocities(10,10)

#Close the serial connection & exit cleanly
board.exit()
"""

import math
import time
import pyfirmata
import serial
import serial.tools.list_ports
from pyfirmata import util


class CodeePy:

    def __init__(self, port):
        """
        The constructor requires the programmer to pass the port name Codee is connected to either via USB(serial) or Bluetooth
        @param port: portname Codee is connected to.
        """
        self.port = port
        # instantiate codee as Pyfirmata object
        self.codee = pyfirmata.Arduino(port)
        self.__set_as_nano()
        # instantiate handler for commands
        self.check_codee_firmware()
        self.codee.add_cmd_handler(pyfirmata.pyfirmata.STRING_DATA, self._messageHandler)

    ######## Call back definition ########

    def _messageHandler(self, *args, **kwargs):
        print("in handler")
        #print (args)
        #print(util.two_byte_iter_to_str(args))
        newres = util.break_to_bytes(args)
        print(util.from_two_bytes(newres))


    ######## Public Functions ########

    def check_codee_firmware(self):
        """
        Checks firmata version is 2.5
        @return True is Firmata is 2.5, False if it is not
        """
        print("Running pyFirmata version:\t%s" % pyfirmata.__version__)
        if self.codee.get_firmata_version()[0] == 2 and self.codee.get_firmata_version()[1] == 5:
            print("Firmata version check passed OK")
            return True
        else:
            return False
    check_codee_firmware.__doc__ = "Check Firmata version is 2.5"

    def say(self, text):
        """
        This method makes Codee "Speak"
        @param text: a string with less than 30 characters that Codee will day
        @return True if Codee "Spoke", else False
        """
        text = text.strip()
        if len(text) < 30:
            saylist = [0x00]
            for x in text:
                saylist.append(ord(x))
            self.codee.send_sysex(0x09, saylist)
            return True
        else:
            print("Please enter text less than 30 characters in length")
            return False
    say.__doc__ = "Generate Audio tone for each char of a string (text)"

    def set_melody_tempo(self, tempo):
        """
        This method sets the tempo of melody playback
        @param tempo: an int tempo value
        """
        tmp = math.floor(tempo * 100)
        # frequency bytes
        tLow = tmp & 0xFF
        tHigh = (tmp & 0xFFFF) >> 8
        self.codee.send_sysex(0x09, [0x04, tHigh, tLow])
    set_melody_tempo.__doc__ = "Set tempo for playback"

    def play_melody(self, melody):
        """
        This method make Codee play preset melodies
        @param melody: preset melody Codee will play
        """
        global song_choice
        if melody == "green sleeves": song_choice = 0x00
        if melody == "little lamb": song_choice = 0x01
        if melody == "happy birthday": song_choice = 0x02
        if melody == "star wars": song_choice = 0x03
        if melody == "chariots": song_choice = 0x04
        self.codee.send_sysex(0x09, [0x01, song_choice])
    play_melody.__doc__ = "Melody variable choices: \n" \
                          "green sleeves \n" \
                          "little lamb \n" \
                          "happy birthday \n" \
                          "star wars \n" \
                          "chariots"

    def play_tone(self, frequency, duration):
        """
        This method makes Codee generate a tone
        @param frequency: int frequency of the tone
        @param duration: int duration of tone
        """
        # frequency bytes
        flow = frequency & 0xFF
        fhigh = (frequency & 0xFFFF) >> 8
        # durationbytes
        dlow = duration & 0xFF
        dhigh = (duration & 0xFFFF) >> 8
        self.codee.send_sysex(0x09, [0x03, fhigh, flow, dhigh, dlow])
    play_tone.__doc__ = "Play a single frequency tone for given milliseconds"

    def play_notes(self, noteList, duration):
        """
        This method will make Codee play notes of a given duration
        @param noteList: a list of note values as strings
        @param duration: int duration each note is played
        """
        # create melody list to hold song data
        melodylist = [0x02]
        # define notes/frequency key value pairs
        notedictionary = {"RST": 0,
                          "C1": 33, "CS1": 35, "D1": 37, "DS1": 39, "E1": 41, "F1": 44, "FS1": 46, "G1": 49, "GS1": 52,
                          "A1": 55, "AS1": 58, "B1": 62,
                          "C2": 65, "CS2": 69, "D2": 73, "DS2": 78, "E2": 82, "F2": 87, "FS2": 93, "G2": 98, "GS2": 104,
                          "A2": 110, "AS2": 117, "B2": 123,
                          "C3": 131, "CS3": 139, "D3": 147, "DS3": 156, "E3": 165, "F3": 175, "FS3": 185, "G3": 196,
                          "GS3": 208, "A3": 220, "AS3": 223, "B3": 248,
                          "C4": 262, "CS4": 277, "D4": 294, "DS4": 311, "E4": 330, "F4": 349, "FS4": 370, "G4": 392,
                          "G34": 415, "A4": 440, "AS4": 466, "B4": 494,
                          "C5": 523, "CS5": 554, "D5": 587, "DS5": 662, "E5": 659, "F5": 698, "FS5": 740, "G5": 784,
                          "GS5": 831, "A5": 880, "AS5": 932, "B5": 988,
                          "C6": 1047, "CS6": 1109, "D6": 1175, "DS6": 1245, "E6": 1319, "F6": 1397, "FS6": 1480,
                          "G6": 1568, "GS6": 1661, "A6": 1760, "AS6": 1865, "B6": 1976,
                          "C7": 2093, "CS7": 2217, "D7": 2349, "DS7": 2489, "E7": 2637, "F7": 2794, "FS7": 2960,
                          "G7": 3136, "GS7": 3322, "A7": 3520, "AS7": 3729, "B7": 3951,
                          "C8": 4186, "CS8": 4435, "D8": 4699, "DS8": 4978}
        for x in noteList:
            frequency = notedictionary.get(x, 0)  # set default value to 0 to avoid key errors
            flow = frequency & 0xFF
            fhigh = (frequency & 0xFFFF) >> 8
            melodylist.append(fhigh)
            melodylist.append(flow)
            melodylist.append(duration)
        self.codee.send_sysex(0x09, melodylist)
    play_notes.__doc__ = "Play notes from passed in List"


    def play_notes_with_duration(self, noteList):
        """
        This method will make Codee play notes of a given duration
        @param noteList: a list of note and duration values as strings delimited by '.'
        """
        # create melody list to hold song data
        melodylist = [0x02]
        # define notes/frequency key value pairs
        notedictionary = {"RST": 0,
                          "C1": 33, "CS1": 35, "D1": 37, "DS1": 39, "E1": 41, "F1": 44, "FS1": 46, "G1": 49, "GS1": 52,
                          "A1": 55, "AS1": 58, "B1": 62,
                          "C2": 65, "CS2": 69, "D2": 73, "DS2": 78, "E2": 82, "F2": 87, "FS2": 93, "G2": 98, "GS2": 104,
                          "A2": 110, "AS2": 117, "B2": 123,
                          "C3": 131, "CS3": 139, "D3": 147, "DS3": 156, "E3": 165, "F3": 175, "FS3": 185, "G3": 196,
                          "GS3": 208, "A3": 220, "AS3": 223, "B3": 248,
                          "C4": 262, "CS4": 277, "D4": 294, "DS4": 311, "E4": 330, "F4": 349, "FS4": 370, "G4": 392,
                          "G34": 415, "A4": 440, "AS4": 466, "B4": 494,
                          "C5": 523, "CS5": 554, "D5": 587, "DS5": 662, "E5": 659, "F5": 698, "FS5": 740, "G5": 784,
                          "GS5": 831, "A5": 880, "AS5": 932, "B5": 988,
                          "C6": 1047, "CS6": 1109, "D6": 1175, "DS6": 1245, "E6": 1319, "F6": 1397, "FS6": 1480,
                          "G6": 1568, "GS6": 1661, "A6": 1760, "AS6": 1865, "B6": 1976,
                          "C7": 2093, "CS7": 2217, "D7": 2349, "DS7": 2489, "E7": 2637, "F7": 2794, "FS7": 2960,
                          "G7": 3136, "GS7": 3322, "A7": 3520, "AS7": 3729, "B7": 3951,
                          "C8": 4186, "CS8": 4435, "D8": 4699, "DS8": 4978}
        for x in noteList:
            frequency, duration = x.split('.')
            frequency = notedictionary.get(frequency, 0)  # set default value to 0 to avoid key errors
            flow = frequency & 0xFF
            fhigh = (frequency & 0xFFFF) >> 8
            melodylist.append(fhigh)
            melodylist.append(flow)
            melodylist.append(int(duration))
        self.codee.send_sysex(0x09, melodylist)
    play_notes.__doc__ = "Play notes from passed in List"

    def swing_arms(self, speed, state):
        """
        This method will make Codee swing his arms
        @param speed: an int value between 0 and 10 inclusive
        @param state: True to swing arms else False
        """
        if speed > 10: speed = 10
        if speed < 0: speed = 0
        self.codee.send_sysex(0x0B, [speed, state])
    swing_arms.__doc__ = "Function to swing arms, speed is speed of swing, state is True) or False"

    def set_right_arm(self, degrees):
        """
        This method will set Codees right arm to given degree
        @param degrees: an int value greater between -90 and 90 inclusive
        """
        if abs(degrees) < 91:
            degrees = 90 + degrees
            self.codee.servo_config(5, 544, 2400, degrees)
            time.sleep(.5)
        else:
            print("Please enter a number between -90 and 90")
    set_right_arm.__doc__ = "Set right servo angle to degrees x"

    def set_left_arm(self, degrees):
        """
        This method will set Codees left arm to given degree
        @param degrees: an int value between -90 and 90 inclusive
        """
        if abs(degrees) < 91:
            degrees = 90 - degrees
            self.codee.servo_config(4, 544, 2400, degrees)
            time.sleep(.5)
        else:
            print("Please enter a number between -90 and 90")
    set_left_arm.__doc__ = "Set left servo angle to degrees x"

    def set_arms(self, leftarm_degree, rightarm_degree):
        """
        This method will set Codees arms to given degrees
        @param leftarm_degree: an int value between -90 and 90 inclusive
        @param rightarm_degree: an int value between -90 and 90 inclusive
        """
        self.set_left_arm(leftarm_degree)
        self.set_right_arm(rightarm_degree)
    set_arms.__doc__ = "Set both arm servo angles to degrees x, y"

    def stop_arms(self):
        """
        This method will stop Codee's arms moving
        """
        self.codee.send_sysex(0x0B, [0, 0])
    stop_arms.__doc__ = "Stop arm movement"

    def look_around(self, speed, state):
        """
        This method will make Codee's head turn from side to side
        @param speed: an int value between 0 and 5 inclusive
        @param state: True to look around else False
        """
        if speed > 5: speed = 5
        if speed < 0: speed = 0
        self.codee.send_sysex(0x0C, [speed, state])
    look_around.__doc__ = "Start head movement"

    def stop_look_around(self):
        """
        This method will stop Codee's head movements
        """
        self.codee.send_sysex(0x0C, [0, 0])
    stop_look_around.__doc__ = "Stop head movement"

    def set_head(self, degrees):
        """
        This method set Codee's head to a given degree
        @param degrees: an int value between -50 and 50 inclusive
        """
        if abs(degrees) < 51:
            degrees = 90 + degrees
            self.codee.servo_config(6, 544, 2400, degrees)
            time.sleep(.5)
        else:
            print("Please enter a number between -50 and 50")
    set_head.__doc__ = "Set head to x position"

    def display_image(self, image):
        """
        This method will make Codee LED matrix display a preset image
        @param image: string value of preset image
        """
        global imagetodisp
        if image == "smile": imagetodisp = 0x00
        if image == "neutral": imagetodisp = 0x01
        if image == "frown": imagetodisp = 0x02
        if image == "question": imagetodisp = 0x03
        if image == "ok": imagetodisp = 0x04
        if image == "tick": imagetodisp = 0x05
        if image == "cross": imagetodisp = 0x06
        if image == "rock": imagetodisp = 0x07
        if image == "paper": imagetodisp = 0x08
        if image == "sissors": imagetodisp = 0x09
        if image == "heart": imagetodisp = 0x0A
        if image == "quaver": imagetodisp = 0x0B
        if image == "quaverx2": imagetodisp = 0x0C
        if image == "blank": imagetodisp = 0x0D
        self.codee.send_sysex(0x0A, [0x01, imagetodisp])
    set_head.__doc__ = "Set head to a image to selected image: \n" \
                          "smile \n" \
                          "neutral \n" \
                          "frown \n" \
                          "question \n" \
                          "ok \n" \
                          "tick \n" \
                          "cross \n" \
                          "paper \n" \
                          "sissors \n" \
                          "heart \n" \
                          "quaver \n" \
                          "quaverx2 \n" \
                          "blank"

    def led_scroll_text(self, text):
        """
        This method will make Codees LED matrix scroll given text
        @param text: text to scroll as string
        """
        text = text.strip()
        if len(text) < 30:
            scroll_list = [0x02, True]
            for x in text:
                scroll_list.append(ord(x))
                self.codee.send_sysex(0x0A, scroll_list)
        else:
            print("Please enter text less than 30 characters in length")
    led_scroll_text.__doc__ = "Scroll text x on Codee head display"

    def display_number(self, number):
        """
        This method will make Codees LED matrix display a number
        @param number: numver to display as int between 0 and 99 inclusive
        """
        if number >= 0 and number <= 99:
            self.codee.send_sysex(0x0A, [0x03, number])
        else:
            print("Please enter a number between 0 and 99")
    display_number.__doc__ = "Display number x on Codee head display"

    def display_clear(self):
        """
        This method will clear Codees LED matrix turning off all LED's
        """
        self.codee.send_sysex(0x0A, [0x06])
    display_clear.__doc__ = "Clear Codee head display"

    def set_led_display_pixel(self, row, column, state):
        """
        This method will set the state of a single LED in  Codees LED matrix
        @param row: row of pixel between 0 and 7 inclusive as int
        @param column: column of pixel between 0 and 7 inclusive as int
        @param state: desired state either True or False
        """
        if column > -1 and column < 8 and row > -1 and row < 8:
            self.codee.send_sysex(0x0A, [0x05, row, column, state])
        else:
            print("Please enter a row and column values between 0 and 7")
    set_led_display_pixel.__doc__ = "Set individual pixel state (True/False)"

    def set_left_wheel_velocity(self, leftspeed):
        """
        This method will set the speed of the left wheel servo
        @param leftspeed: wheel speed between 0 and 180 inclusive as int
        """
        leftspeed = 90 + leftspeed
        if leftspeed < 0:
            leftspeed = 0
        if leftspeed > 180:
            leftspeed = 180
        self.codee.send_sysex(0x0E, [leftspeed, 0x00])
    set_left_wheel_velocity.__doc__ = "Set left wheel velocity"

    def set_right_wheel_velocity(self, rightspeed):
        """
        This method will set the speed of the right wheel servo
        @param rightspeed: wheel speed between 0 and 180 inclusive as int
        """
        rightspeed = 90 - rightspeed
        if rightspeed < 0:
            rightspeed = 0
        if rightspeed > 180:
            rightspeed = 180
        self.codee.send_sysex(0x0E, [0x00, rightspeed])
    set_right_wheel_velocity.__doc__ = "Set right wheel velocity"

    def set_wheel_velocities(self, leftspeed, rightspeed):
        """
        This method will set the speed of both wheel servos
        @param leftspeed: wheel speed between 0 and 180 inclusive as int
        @param rightspeed: wheel speed between 0 and 180 inclusive as int
        """
        self.set_right_wheel_velocity(rightspeed)
        self.set_left_wheel_velocity(leftspeed)
    set_wheel_velocities.__doc__ = "Set bothe wheel velocities, leftspeed rightspeed"

    def stop_wheels(self):
        """
        This method will stop both wheel servos
        """
        self.codee.send_sysex(0x0E, [0x5A, 0x5A])
    stop_wheels.__doc__ = "Stop wheels"

    def change_bot_bluetooth_name(self, text):
        """
        This method will change the bluetooth name of your Codee
        @param text: new name as string
        """
        text = text.strip()
        if len(text) < 11:
            btlist = [1]
            # btlist = [01]
            for x in text:
                btlist.append(ord(x))
            self.codee.send_sysex(0x0D, btlist)
            time.sleep(8)
            self.codee.exit()
            print("Your robot is now named " + text)
        else:
            print("Please enter text less than 10 characters in length")
    change_bot_bluetooth_name.__doc__ = "Change Bluetooth name"

    def read_line_sensor(self, sensor_id, duration):
        """
        This method will read the value of one line sensor
        Prints results, no return, for testing only
        0.0 min value = black, 1.0 max value = white
        @param sensor_id: line senor if as int
        @param duration: time you would like to read line sensor
        """
        global pin_setup
        if sensor_id == 1: pin_setup = 'a:2:i'
        if sensor_id == 2: pin_setup = 'a:3:i'
        if sensor_id == 3: pin_setup = 'a:4:i'
        if sensor_id == 4: pin_setup = 'a:5:i'
        if sensor_id == 5: pin_setup = 'a:6:i'
        it = util.Iterator(self.codee)
        it.start()
        line_sensor = self.codee.get_pin(pin_setup)
        try:
            for x in range(duration*4):
                time.sleep(0.25)  #time in secs betweens reads
                p = line_sensor.read()
                print(p)
        except KeyboardInterrupt:
            self.codee.exit()
    read_line_sensor.__doc__ = "Continual read of line IR sensor"

    def read_line_position(self, no_sensors):
        """
        This method will set the speed of both wheel servos
        @param no_sensors: no_sensor is either 3 or 5 as int
        @return array of int values 1 = black 0 = white
        """
        global sensor_result1, sensor_result2, sensor_result3, sensor_result4, sensor_result5, output_arr
        output_arr = []
        results_are_none = True

        if(no_sensors == 3 or no_sensors == 5):
            line_sensor_1 = self.codee.get_pin('a:2:i')
            line_sensor_2 = self.codee.get_pin('a:3:i')
            line_sensor_3 = self.codee.get_pin('a:4:i')
            line_sensor_4 = self.codee.get_pin('a:5:i')
            line_sensor_5 = self.codee.get_pin('a:6:i')
            it = util.Iterator(self.codee)
            it.start()
            try:
                while results_are_none:
                    time.sleep(0.05)
                    if(no_sensors == 5):
                        sensor_result1 = line_sensor_1.read()
                        print(sensor_result1)
                        if sensor_result1 is not None:
                            sensor_result1 = 1 if sensor_result1 < 0.5 else 0
                            output_arr.append(sensor_result1)
                    sensor_result2 = line_sensor_2.read()
                    print(sensor_result2)
                    if sensor_result2 is not None:
                        sensor_result2 = 1 if sensor_result2 < 0.5 else 0
                        output_arr.append(sensor_result2)
                    sensor_result3 = line_sensor_3.read()
                    print(sensor_result3)
                    if sensor_result3 is not None:
                        sensor_result3 = 1 if sensor_result3 < 0.5 else 0
                        output_arr.append(sensor_result3)
                    sensor_result4 = line_sensor_4.read()
                    print(sensor_result4)
                    if sensor_result4 is not None:
                        sensor_result4 = 1 if sensor_result4 < 0.5 else 0
                        output_arr.append(sensor_result4)
                    if no_sensors == 5:
                        sensor_result5 = line_sensor_5.read()
                        print(sensor_result5)
                        if sensor_result5 is not None:
                            sensor_result5 = 1 if sensor_result5 < 0.5 else 0
                            output_arr.append(sensor_result5)
                    if no_sensors == 3 and len(output_arr) == 3:
                        results_are_none = False
                    if no_sensors == 5 and len(output_arr) == 5:
                        results_are_none = False
            except KeyboardInterrupt:
                self.codee.exit()
            return output_arr
        else:
            print("no of sensors must be 3 or 5")
            return output_arr
    read_line_position.__doc__ = "returns an array of all the sensor values that detect a black line, 1 is true 0 is false"

    def set_led_display_rows(self, hex):
        """
        This method will set the display rows
        @param hex: input row as hex
        """
        if len(hex) == 16:
            self.codee.send_sysex(0x0A, [0x04])
        else:
            print("Please enter 16 hex digits")
    set_led_display_rows.__doc__ = "Set active display rows"

    def reset_codee_body_and_exit(self):
        """
        This method will reset Codees limbs to default position
        stop head, wheel movements and clear the display then disconnect codee
        """
        self.stop_arms()
        self.set_right_arm(-90)
        self.set_left_arm(-90)
        self.stop_look_around()
        self.set_head(0)
        self.stop_wheels()
        self.display_clear()
        self.exit()
    reset_codee_body_and_exit.__doc__ = "Reset codee's body and disconnect"

    def robot_ultrasound_distance_reading(self):
        """
        This method is still in development
        """
        data = []
        # start ultrasound
        self.codee.send_sysex(0x08, data)
        print("sent sysex")
        it = util.Iterator(self.codee)
        it.start()
        try:
            #while self.codee.bytes_available():
            if self.codee.bytes_available():
                self.codee.iterate()
                time.sleep(0.2)  # time in secs betweens reads
        except KeyboardInterrupt:
            self.codee.exit()

    ######## Helper Functions ########

    @staticmethod
    def get_com_ports():
        """
        Can be called as a static class method to obtain COM ports on windows
        @return a list of COM ports (string)
        """
        print("COM port list")
        portlist = list(serial.tools.list_ports.comports())
        for p in portlist:
            print(p)
        return portlist
    get_com_ports.__doc__ = "Get list of available COM ports"

    def exit(self):
        self.codee.exit()
    exit.__doc__ = "Exit and disconnect port"

    def __set_as_nano(self):
        """
        Sets board spec to nano
        """
        nano = {
            'digital': tuple(x for x in range(14)),
            'analog': tuple(x for x in range(8)),
            'pwm': (3, 5, 6, 9, 10, 11),
            'use_ports': True,
            'disabled': (0, 1)  # Rx, Tx, Crystal
        }
        self.codee.setup_layout(nano)

