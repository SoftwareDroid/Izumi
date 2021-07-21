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

from enum import Enum

class ParseResult(Enum):
    COMMAND_ACCEPTED = 0
    COMMAND_ACCEPTED_SILENT = 6,
    # No valid command forward to other modul
    TRIGGER_WORD_MISSING = 1
    # Show show error
    VERB_MISSING = 2
    # Show error
    ARGUMENT_ERROR = 3
    FUNCTIONALITY_MISSING = 4
    PERMISSION_DENIED_SILENT = 5
