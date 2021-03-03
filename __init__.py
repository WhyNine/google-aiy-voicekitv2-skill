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
colours = [Color.RED, Color.GREEN, Color.YELLOW, Color.BLUE, Color.PURPLE, Color.CYAN, Color.WHITE, Color.BLACK]

class PicroftGoogleAiyVoicekitv2(MycroftSkill):

    def led_idle(self):
        self.log.info("Change LED to IDLE colour")
        self.leds.update(Leds.rgb_on(Color.blend(colours[self.ledidlecolour], Color.BLACK, self.ledidleintensity/100)))

    def led_listen(self):
        self.log.info("Change LED to LISTEN colour")
        self.leds.update(Leds.rgb_on(Color.blend(colours[self.ledlistencolour], Color.BLACK, self.ledlistenintensity/100)))

    def led_think(self):
        self.log.info("Change LED to THINK colour")
        self.leds.update(Leds.rgb_on(Color.blend(colours[self.ledthinkcolour], Color.BLACK, self.ledthinkintensity/100)))

    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        self.settings_change_callback = self.on_settings_changed
        self.get_settings()
        try:
            self.leds = Leds()
            self.led_idle()
        except:
            self.log.warning("Can't initialize LED - skill will not load")
            self.speak_dialog("error.initialize")
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.remove_event_detect(BUTTON)
            GPIO.add_event_detect(BUTTON, GPIO.FALLING, bouncetime = 500)
        except:
            self.log.warning("Can't initialize GPIO - skill will not load")
            self.speak_dialog("error.initialize")
        finally:
            self.schedule_repeating_event(self.button_press, None, 0.1, 'GoogleAIYv2')
            self.add_event('recognizer_loop:record_begin', self.on_listener_started)
            self.add_event('recognizer_loop:record_end', self.on_listener_ended)
            self.add_event('mycroft.skill.handler.complete', self.on_handler_complete)

    def button_press(self, message):
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

    def on_listener_started(self, message):
        self.led_listen()

    def on_listener_ended(self, message):
        self.led_think()

    def on_handler_complete(self, message):
        self.led_idle()

    def on_settings_changed(self):
        self.get_settings()
        self.led_idle()
        
    def get_settings(self):
        self.ledidlecolour = int(self.settings.get('ledidlecolour', 1))
        self.ledidleintensity = self.settings.get('ledidleintensity', 100)
        if self.ledidleintensity < 0: self.ledidleintensity = 0 
        if self.ledidleintensity > 100: self.ledidleintensity = 100 
        self.ledlistencolour = int(self.settings.get('ledlistencolour', 2))
        self.ledlistenintensity = self.settings.get('ledlistenintensity', 100)
        if self.ledlistenintensity < 0: self.ledlistenintensity = 0 
        if self.ledlistenintensity > 100: self.ledlistenintensity = 100
        self.ledthinkcolour = 0
        self.ledthinkintensity = 100


def create_skill():
    return PicroftGoogleAiyVoicekitv2()
