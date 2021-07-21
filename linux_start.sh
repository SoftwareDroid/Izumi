#!/bin/bash
# Set my usb headset as process source
pactl set-default-source "alsa_input.usb-GeneralPlus_USB_Audio_Device-00.mono-fallback"

# Start server
libretranslate &
# Change working dir for pipenv
cd /home/patrick/projects/ConvientVoiceDictation/

# we have to use abolute paths because we have a limited enviroment in cron          
pipenv run python main.py  -key "AIzaSyDRYsXg8qj8PfhuWFYKA-cRAnPDn5j4tJo" -profile "profiles/example.json"

