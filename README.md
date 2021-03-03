# <img src='AIY_logo_blue.png' card_color='#022B4F' width='50' height='50' style='vertical-align:bottom'/> Google AIY voicekitv2
Enables Google AIY voicekit v2 (with Voice Bonnet)

## About
This enables the LED and button on the Google AIY voicekit v2 (with Voice Bonnet, NOT Voice HAT).

The colour and intensity of the LED in the button can be set for when Mycroft is idle (waiting for the wake-up phrase), when it is listening (waiting for a command) and when it is thinking (working out which skill can handle the command). If the button is pressed, Mycroft begins to listen. If the button is pressed for a longer time, it stops whatever it is doing.

## Important
This skill is made for Picroft Lightning, which is Picroft on Rasbian Stretch. It assumes that the Voice Bonnet is already installed.

The following commands may need to be run to ensure that the Python aiy modules can be found:
* git clone https://github.com/google/aiyprojects-raspbian.git AIY-projects-python
* sudo pip3 install -e AIY-projects-python/src
* echo "/home/pi/AIY-projects-python/src" > ~/mycroft-core/.venv/lib/python3.7/site-packages/aiy.pth

## Category
**IoT**

## Credits
Simon Waller (but based on the work by Andreas Lorensen (@andlo) for the original version for the Voice HAT).

## Supported Devices
platform_picroft

## Tags
#googlevoicekit
#aiy
#Googleaiy
#voicekit
#voicebonnet

