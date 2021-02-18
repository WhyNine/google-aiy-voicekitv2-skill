"""
skill picroft-google-aiy-voicekitv2
Copyright (C) 2018  Andreas Lorensen

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from mycroft import MycroftSkill
from mycroft.messagebus.message import Message

import time
import RPi.GPIO as GPIO
from aiy.leds import Leds, Color

# GPIO pins
BUTTON = 23

class PicroftGoogleAiyVoicekitv2(MycroftSkill):

    def __init__(self):
        self.leds = Leds()
        MycroftSkill.__init__(self)

    def initialize(self):
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.remove_event_detect(BUTTON)
            GPIO.add_event_detect(BUTTON, GPIO.FALLING, bouncetime = 500)
            self.leds.update(Leds.rgb_on(Color.GREEN))
        except GPIO.error:
            self.log.warning("Can't initialize GPIO - skill will not load")
            self.speak_dialog("error.initialise")
        finally:
            self.schedule_repeating_event(self.handle_button,
                                          None, 0.1, 'GoogleAIYv2')
            self.add_event('recognizer_loop:record_begin',
                           self.handle_listener_started)
            self.add_event('recognizer_loop:record_end',
                           self.handle_listener_ended)

    def handle_button(self, message):
        longpress_threshold = 2
        if GPIO.event_detected(BUTTON):
            self.log.info("GPIO.event_detected")
            pressed_time = time.time()
            while not GPIO.input(BUTTON):
                time.sleep(0.2)
            pressed_time = time.time() - pressed_time
            if pressed_time < longpress_threshold:
                self.bus.emit(Message("mycroft.mic.listen"))
            else:
                self.bus.emit(Message("mycroft.stop"))

    def handle_listener_started(self, message):
        # code to excecute when active listening begins...
        self.log.info("Turn LED white")
        self.leds.update(Leds.rgb_on(Color.WHITE))

    def handle_listener_ended(self, message):
        self.leds.update(Leds.rgb_on(Color.GREEN))


def create_skill():
    return PicroftGoogleAiyVoicekitv2()
