import asyncio, logging

logging.basicConfig(level=logging.INFO)

from core.network import Network

from flet import *

from core.authorization import Authorization
from core.profile_manager import ProfileManager
from ui.components.view_manager import ViewManager
from ui.components.settings import Settings
from ui.components.word import Word
from ui.dialogs.dialog import Dialog
from core.storage import Storage


class App:
    def __init__(self, page: Page):
        self.page = page

        self.page.padding = 0
        self.page.window.title_bar_hidden = True

        self.page.theme = Theme(
            icon_button_theme=IconButtonTheme(style=ButtonStyle(shape=RoundedRectangleBorder(radius=8))),
            button_theme=ButtonTheme(style=ButtonStyle(shape=RoundedRectangleBorder(radius=8))),
            dialog_theme=DialogTheme(shape=RoundedRectangleBorder(radius=8)),
            popup_menu_theme=PopupMenuTheme(shape=RoundedRectangleBorder(radius=8))
        )

        self.auth = Authorization(self)

        self.storage = Storage(self)
        self.net = Network(self)
        self.set = Settings(self)
        self.word = Word(self)
        self.dlg = Dialog(self)
        self.pm = ProfileManager(self)

        self.view = ViewManager(self)

    def get(self, key: str):
        return self.word.get(key)



if __name__ == '__main__':
    asyncio.run(run_async(App))
