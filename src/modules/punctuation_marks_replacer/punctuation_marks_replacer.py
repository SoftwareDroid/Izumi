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
from src.modules.punctuation_marks_replacer.replacement_table import replacement_table

class PunctuationMarksReplacer(ModuleInterface):
    def __init__(self, activated: bool, settings):
        ModuleInterface.__init__(self, activated=activated, settings=settings)
        self._capilalize = True
        self._add_space = False


    def process(self, text: str) -> str:
        assert "language" in self.settings, "language for replacer not defined"
        lang: str = self.settings["language"]
        assert lang in replacement_table, " language not found " + replacement_table.keys()
        local_table = replacement_table[lang]
        for entry in local_table:
            text = text.replace(entry[0], entry[1])

        auto_capitalize = self.settings.get("sentence-begin-capitalize", True)
        if auto_capitalize:
            #self._capilalize = text.startswith(".") or text.startswith("!") or text.startswith("?")
            if self._capilalize and len(text) > 1:
                text = text[0].upper() + text[1:]
            #if self._add_space and len(text) > 1:
            #    text = " " + text
            # Next
            self._capilalize = text.endswith(".") or text.endswith("!") or text.endswith("?")
            self._add_space = True
            #self._add_space = self._capilalize or (not text.endswith(" "))

        return text
