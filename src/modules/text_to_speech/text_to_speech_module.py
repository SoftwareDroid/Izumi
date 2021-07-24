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

from src.modules.module_interface import ModuleInterface
from src.partial_formatter import PartialFormatter
from src.sentence_parser import SentenceParser
from src.parse_result import ParseResult
from pydub import AudioSegment
from gtts import gTTS
import threading
import pygame
import queue


class TextToSpeechModule(ModuleInterface):
    _FILE = "tmp/tmp_tts"
    def __init__(self, activated: bool, settings):
        ModuleInterface.__init__(self, activated=activated, settings=settings)
        self.queue = queue.Queue()
        self._run = True

        thread = threading.Thread(target=self._play)
        thread.daemon = True
        thread.start()

    def __del__(self):
        self._run = False

    def _play(self):
        while self._run:
            text = self.queue.get()
            self.queue.task_done()
            file: str = TextToSpeechModule._FILE

            slow: bool = self.settings["slow"]
            lang = self.settings["language"]
            tts = gTTS(text, lang=lang, slow=slow)
            tts.save(file + ".mp3")
            AudioSegment.from_mp3(file + ".mp3").export(file + ".wav", format="wav")
            # play
            #print(file + ".wav")
            pygame.mixer.music.load(file + ".wav")
            pygame.mixer.music.play()

    def _replay(self, s: str, v: str, data: str) -> ParseResult:
        try:
            pygame.mixer.music.load(TextToSpeechModule._FILE + ".wav")
            pygame.mixer.music.play()
        except:
            return  ParseResult.ARGUMENT_ERROR
        return ParseResult.COMMAND_ACCEPTED_SILENT

    def register_voice_commands(self, sentence_parser : SentenceParser):
        sentence_parser.register_action(id(self), "replay", self._replay)

    def process(self, text: str) -> str:
        self.queue.put(text)
        return text


