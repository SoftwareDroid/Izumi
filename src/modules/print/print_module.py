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


class PrintModule(ModuleInterface):
    def process(self, text: str) -> str:
        if "format" in self.settings:
            fmt = PartialFormatter()
            text = fmt.format(self.settings["format"], **self.module_variables)
        print(text)
        return text
