# -*- coding: utf-8 -*-
#
# Copyright (c) 2021 Patrick Mispelhorn <patrick.mispelhorn@web.de>
#
# Izumi is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Izumi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# from src.modules.dictation.dictate_module import DictateModule
from src.profile_loader import ProfileLoader
import pygame.mixer
from src.controller import Controller
from src.speech_to_text import SpeechToText
import time
import sys
import os
import argparse
from src.server import RemoteQueueServer
import threading

def main():




    parser = argparse.ArgumentParser(description='Izumi a personal assistant')
    parser.add_argument('-key', metavar="GOOGLE_API_KEY", type=str,
                        help="An key for accessing a speech to text API. An default will be used if not set.")
    parser.add_argument('-profile', dest="profile_name", required=True, metavar="FILE", type=str,
                        help='path to a profile for setting up the pipeline')
    parser.add_argument('--server', dest="server",nargs='?',
                        help='starts remote control')
    #parser.add_argument('-port', dest="profile_name", required=True, metavar="FILE", type=str,
    #                    help='path to a profile for setting up the pipeline')

    args = parser.parse_args()
    print("Server: ",args.server)

        #

    # init sound output
    pygame.init()
    pygame.mixer.init()

    controller: Controller = Controller(args)
    speechToTextModule = SpeechToText(args)
    speechToTextModule.start()
    profile_loader = ProfileLoader(controller=controller, speechToText=speechToTextModule)
    controller.profileLoader = profile_loader
    # Load Profile
    assert profile_loader.load_profile(args.profile_name) , "Profile load failed!"
    port = 47193
    if args.server:
        server = RemoteQueueServer(speechToTextModule.voice_commands,port)
        server.run()


    while controller.get_mode() != Controller.Mode.POWER_OFF:
        text = speechToTextModule.voice_commands.get()
        speechToTextModule.voice_commands.task_done()
        controller.parse(text)

        #events = pygame.event.get()

        # print("Process voice command" ,text)
    if args.server:
        server.stop()
    print("Shutdown ...")
    # calling this function requests that the background listener stop listening
    speechToTextModule.shutdown()

    # do some more unrelated things
    # we're not listening anymore, even though the background thread might still be running for a second or two while cleaning u
    for _ in range(0, 30):
        time.sleep(0.1)
    h.join()
    print("Shutdown complete")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
