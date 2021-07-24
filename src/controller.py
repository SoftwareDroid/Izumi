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

from src.sentence_parser import SentenceParser
# from src.parameters import SYSTEM_NAME
from src.parse_result import ParseResult
from src.modules.module_interface import ModuleInterface
from typing import List
import pygame
from enum import Enum
from src.profile_loader_interface import ProfileLoaderInterface


class Controller:
    DEFAULT_SYSTEM_NAME = "Izumi"
    VERSION_MAJOR: int = 1
    VERSION_MINOR: int = 0

    class Mode(Enum):
        AWAKE = 0
        SLEEPING = 1
        POWER_OFF = 2

    WAKE_UP_COMMAND: str = "wake up"

    def __init__(self, args):
        self.module_variables = {}
        self.profileLoader: ProfileLoaderInterface = None
        self._args = args
        self._mode: Controller.Mode = Controller.Mode.AWAKE
        self._sentence_parser: SentenceParser = SentenceParser(Controller.DEFAULT_SYSTEM_NAME, self._check_module_permission)
        self._all_modules: List[ModuleInterface] = []
        self._register_actions()
        self._ignore_input = []

        self.system_language = "english"
        self.debug_output: bool = False
        self.profile_is_read_only: bool = False

    def _register_actions(self):
        # add default verbs
        #self._sentence_parser.register_action(id(self), "initialize", self._command_start_module)
        # self._sentence_parser.register_action(id(self), "enable", self._command_start_module)

        #self._sentence_parser.register_action(id(self), "disable", self.command_stop_module)
        self._sentence_parser.register_action(id(self), Controller.WAKE_UP_COMMAND, self._command_awake)
        self._sentence_parser.register_action(id(self), "go to sleep", self._command_go_to_sleep)
        self._sentence_parser.register_action(id(self), ["shutdown", "power off", "power of"], self._command_power_off)
        self._sentence_parser.register_action(id(self), "load Profile", self._command_load_profile)

    def set_subject_name(self, name : str):
        self._sentence_parser.set_subject({name})

    def get_mode(self) -> Mode:
        return self._mode

    def _command_load_profile(self, s: str, v: str, data: str) -> ParseResult:
        data = data.lower()
        dir = "profiles/"
        data = data.strip(" ")
        data = data.replace(" ","_")
        data = data + ".json"
        filename = dir + data
        print("Filename: ",data)

        if self.profileLoader.load_profile(filename):
            return ParseResult.COMMAND_ACCEPTED
        else:
            return ParseResult.ARGUMENT_ERROR

    def clear_pipeline(self):
        self._mode = Controller.Mode.AWAKE
        self._sentence_parser: SentenceParser = SentenceParser(Controller.DEFAULT_SYSTEM_NAME, self._check_module_permission)
        self._register_actions()
        self._all_modules: List[ModuleInterface] = []

    def parse(self, text: str):
        """True process """
        for prefix in self._ignore_input:
            if text.startswith(prefix):
                print("Info ignore input: ",text)
                return
        print("Info Parse: ", text)
        results = self._sentence_parser.parse(text)
        actions = {ParseResult.FUNCTIONALITY_MISSING: self._show_error_missing_functionality,
                   ParseResult.ARGUMENT_ERROR: self._show_error_arg_error,
                   ParseResult.VERB_MISSING: self._show_error_verb_missing,
                   ParseResult.PERMISSION_DENIED_SILENT: lambda x: x,  # Ignore output
                   ParseResult.COMMAND_ACCEPTED_SILENT: lambda  x: x,
                   ParseResult.COMMAND_ACCEPTED: self._show_hint_command_accepted}
        # An process can trigger multiple results
        for result in results:
            if result in actions:
                actions[result](text)
            elif result == ParseResult.TRIGGER_WORD_MISSING:
                self._forward_input_to_current_module(text)
            else:
                assert False, "Parse Result undefined"

    def append_module(self, m: ModuleInterface):
        m.module_variables = self.module_variables
        m.register_voice_commands(sentence_parser=self._sentence_parser)
        self._all_modules.append(m)

    def _check_module_permission(self, key: int, subject: str, verb: str, arg: str) -> bool:
        # Only the main module is allowed to execute commands while in sleeping mode
        if self._mode == Controller.Mode.SLEEPING:
            if key != id(self) or verb != Controller.WAKE_UP_COMMAND:
                return False
        return True

    def _command_start_module(self, s: str, v: str, data: str) -> ParseResult:
        for m in self._all_modules:
            if m.test_activation(data):
                m.activated = True
                m.initialize(self._sentence_parser)
                return ParseResult.COMMAND_ACCEPTED
        return ParseResult.ARGUMENT_ERROR

    def _command_go_to_sleep(self, s: str, v: str, data: str) -> ParseResult:
        self._mode = Controller.Mode.SLEEPING
        return ParseResult.COMMAND_ACCEPTED

    def _command_awake(self, s: str, v: str, data: str) -> ParseResult:
        self._mode = Controller.Mode.AWAKE
        return ParseResult.COMMAND_ACCEPTED

    def _command_power_off(self, s: str, v: str, data: str) -> ParseResult:
        self._mode = Controller.Mode.POWER_OFF
        return ParseResult.COMMAND_ACCEPTED

    def command_stop_module(self, s: str, v: str, data: str) -> ParseResult:
        for m in self._all_modules:
            if m.test_activation(data):
                m.activated = False
                m.deactivate(self._sentence_parser)
                return ParseResult.COMMAND_ACCEPTED
        return ParseResult.ARGUMENT_ERROR

    def _forward_input_to_current_module(self, text: str):
        self.module_variables.clear()
        for m in self._all_modules:
            if m.activated:
                print(m)
                # Save process and output if idenifier is set
                if m.identifier is not None:
                    self.module_variables["{}_in".format(m.identifier)] = text
                text = m.process(text)
                if m.identifier is not None:
                    self.module_variables["{}_out".format(m.identifier)] = text
                if text is None:
                    print("pipeline abort")
                    break

    def _show_hint_command_accepted(self, text):
        pygame.mixer.music.load("assets/misc_menu.wav")
        pygame.mixer.music.play()
        print("command accepted ", text)

    def _show_error_verb_missing(self, text):
        print("Error: command lacks of a verb ", text)
        pygame.mixer.music.load("assets/negative.wav")
        pygame.mixer.music.play()

    def _show_error_arg_error(self, text):
        print("Error: arg error ", text)
        pygame.mixer.music.load("assets/negative.wav")
        pygame.mixer.music.play()

    def _show_error_missing_functionality(self, text):
        print("Error: Missing functionality", text)
        pygame.mixer.music.load("assets/negative.wav")
        pygame.mixer.music.play()

