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
import requests
import json


class OfflineTranslatorModule(ModuleInterface):
    def __init__(self, activated: bool, settings):
        ModuleInterface.__init__(self, activated=activated,settings=settings)

    def process(self, text: str) -> str:
        source = self.settings["input-language"]
        target= self.settings["output-language"]
        url = "http://localhost:5000/translate"
        body = {'source': source, 'target': target, 'q': text}
        print(body)#möge die Macht mit dir sein
        headers = { "Content-Type": "application/json"}
        data = json.dumps(body,ensure_ascii=False).encode('utf-8')
        try:
            r = requests.post(url, data=data, headers=headers)
            if r.status_code == 200:
                ret = r.json()['translatedText']
                print(ret)
            else:
                print("Error: ", r.status_code, r.reason)
                return None
        except requests.exceptions.ConnectionError:
            print("Error: Translation Server not found!")
            return None
        return ret
