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

from typing import List, Set, Dict, Tuple, Optional, Callable
from src.parse_result import ParseResult
from collections.abc import Iterable

class SentenceParser:

    def __init__(self, subjects : Set[str] , check_permission : Callable[[int,str,str,str],bool]):
        # Key -> Dict[verb,func[subject,verb,rest]]
        self._key_to_verb_to_actions: Dict[tuple[int, Dict[tuple[str, Callable[[str, str, str], None]]]]] = dict()
        self._subjects: Set[str] = set()
        # verb -> Set[keys]
        self._verb_to_object : Dict[tuple[str,List[int]]] = dict()
        self._check_permission = check_permission
        for s in subjects:
            self._subjects.add(s.lower())

    def set_subject(self,subjects: Set[str]):
        self._subjects: Set[str] = set()
        for s in subjects:
            self._subjects.add(s.lower())

    def register_action(self, key : int, verbs : List[str], action : Callable[[str, str, str], None]):
        """verb = (subject,verb,argument)"""
        # accept also single strings
        if type(verbs) == str:
            verbs = [verbs]
        verbs = [x.lower() for x in verbs]
        for verb in verbs:
            if key not in self._key_to_verb_to_actions:
                self._key_to_verb_to_actions[key] = dict()
            self._key_to_verb_to_actions[key][verb] = action
            if verb not in self._verb_to_object:
                self._verb_to_object[verb] = list()
            assert key not in self._verb_to_object[verb], "Module with same id already registered" + key
            self._verb_to_object[verb].append(key)

    #def deregister_verb(self,key: int):
    #    self._verb_to_actions.pop(key)

    def parse(self, text: str) -> List[ParseResult]:
        subject = None
        verb = None
        text = text.lower()
        # Get subject
        for s in self._subjects:
            if text.startswith(s):
                subject = s
                text = text[len(s):].lstrip()
                break
        if subject is None:
            return [ParseResult.TRIGGER_WORD_MISSING]
        # TODO FIX ME map empty

        for v in self._verb_to_object.keys():
            if text.startswith(v):
                verb = v
                text = text[len(v):].lstrip()
                break
        if verb is None:
            return [ParseResult.VERB_MISSING]

        rest = text.lstrip()
        result = []
        for key in self._verb_to_object[verb]:
            if self._check_permission(key, subject, verb, rest):
                result.append(self._key_to_verb_to_actions[key][verb](subject, verb, rest))
            else:
                result.append(ParseResult.PERMISSION_DENIED_SILENT)
        return result


#parser : SentenceParser = SentenceParser({"Izumi"})
#parser.register_action("switch to",action)
#parser.parse("Izumi switch to dication mode")

