# <img src='AIY_logo_blue.png' card_color='#022B4F' width='50' height='50' style='vertical-align:bottom'/> Google AIY voicekitv2
Enables Google AIY voicekit v2 (with Voice Bonnet)

## About
This enables the led and button on the Google AIY voicekit v2.

The button led turns on when Mycroft is listening. If button is pressed he begins to listen. If the button is pressed for a longer time he stops whatever he is doing.

## Important
This skill is made for Picroft Lightning which is Picroft on Rasbian Stretch and should install and initialize "out of the box", assuming that the Voice Bonnet is already working for voice input and speaker output.

The following commands may need to be run to ensure that the aiy modules can be found:
* git clone https://github.com/google/aiyprojects-raspbian.git AIY-projects-python
* sudo pip3 install -e AIY-projects-python/src
* echo "/home/pi/AIY-projects-python/src" > ~/mycroft-core/.venv/lib/python3.7/site-packages/aiy.pth

## Category
**IoT**

## Credits
Andreas Lorensen (@andlo) for the original version (for the Voice HAT).
Simon Waller for the modified version (for the Voice Bonnet).

## Supported Devices
platform_picroft

## Tags
#googlevoicekit
#aiy
#Googleaiy
#voicekit
#voicebonnet

