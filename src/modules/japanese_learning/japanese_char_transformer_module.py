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
import pykakasi
from src.partial_formatter import PartialFormatter

class JapaneseCharTransformerModule(ModuleInterface):
    def __init__(self, activated: bool, settings):
        ModuleInterface.__init__(self, activated=activated,settings=settings)
        self.kks = pykakasi.kakasi()

    def process(self, text: str) -> str:
        result = self.kks.convert(text)
        orig = ""
        kana = ""
        hiragana = ""
        romaji = ""
        space = ""
        if self.settings["use-spaces"]:
            space = " "
        for item in result:
            orig = orig + space+item['orig']
            kana = kana + space+item['kana']
            hiragana = hiragana + space+item['hira']
            romaji = romaji + space+item['hepburn']
        self.module_variables["hira"] = hiragana.lstrip()
        self.module_variables["kana"] = kana.lstrip()
        self.module_variables["orig"] = orig.lstrip()
        self.module_variables["kana"] = kana.lstrip()
        self.module_variables["romaji"] = romaji.lstrip()
        fmt = PartialFormatter()
        ret = fmt.format(self.settings["format"],**self.module_variables)
        return ret

