#  Copyright 2020 Maxim Pavlov
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from time import time
from enum import Enum
from krita import Extension
from PyQt5.QtCore import QTimer
from .pypresence import Presence


def register():
    Krita.instance().addExtension(DiscordExtension(Krita.instance()))


class KritaLogo(Enum):
    BASE = 'krita-base'


class DiscordExtension(Extension):
    DISCORD_APP_CLIENT_ID = '782576930591211541'  # https://discord.com/developers/applications/

    def __init__(self, parent):
        super().__init__(parent)
        self.destroyed.connect(self._destroy)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_presence)
        self._presence = Presence(self.DISCORD_APP_CLIENT_ID)
        self._last_opened_file = ''

    def setup(self):
        self._presence.connect()
        self._timer.start(5000)

    def createActions(self, window):
        pass

    def _update_presence(self):
        if Krita.instance().activeDocument() is None:
            self._presence.update(details='Idling...', large_image=KritaLogo.BASE.value)
            self._last_opened_file = ''
        else:
            file_path = Krita.instance().activeDocument().fileName()
            if self._last_opened_file != file_path:
                file_name = Krita.instance().activeDocument().name()
                self._presence.update(
                    details='Drawing something epic',
                    state=file_name if file_name else 'Unnamed',
                    large_image=KritaLogo.BASE.value,
                    start=int(time())
                )
                self._last_opened_file = file_path

    def _destroy(self):
        #  TODO
        self._timer.stop()
        self._presence.close()


register()
