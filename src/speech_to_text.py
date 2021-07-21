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

import queue

import speech_recognition as sr
import pygame
# TODO Problem es wird immer das default micro genommen.
class SpeechToText:
    def __init__(self,args):
        self.voice_commands = queue.Queue()
        self.args = args
        self.input_language = ""
        self.print_errors = False
        if args.key is None:
            print("Use default Google API Key")
        else:
            print("Use API-KEY: ", args.key)

    def start(self):
        m = sr.Microphone()
        r = sr.Recognizer()


        with m as source:
            r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening

        # start listening in the background (note that we don't have to do this inside a `with` statement)
        self._stop_listening = r.listen_in_background(m,self._callback, phrase_time_limit=None)
        print("Start Listening...")

    def shutdown(self):
        self._stop_listening(wait_for_stop=False)
        # clear queue
        while not self.voice_commands.empty():
            self.voice_commands.get()
            self.voice_commands.task_done()
        # close queue
        self.voice_commands.join()

    def _callback(self, recognizer, audio):
        #print("Info: Listener callback")
        # received audio data, now we'll recognize it using Google Speech Recognition
        try:
            text = recognizer.recognize_google(audio, key=self.args.key, language= self.input_language)
            self.voice_commands.put(text)
        except sr.UnknownValueError:
            if self.print_errors:
                pygame.mixer.music.load("../assets/negative.wav")
                pygame.mixer.music.play()
                print("Debug: Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            if self.print_errors:
                pygame.mixer.music.load("../assets/negative.wav")
                pygame.mixer.music.play()
                print("Debug: Could not request results from Google Speech Recognition service; {0}".format(e))
        except NotImplementedError:
            pass