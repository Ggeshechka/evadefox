import asyncio
from typing import TYPE_CHECKING

from flet import *

from configs.languages import languages

if TYPE_CHECKING:
    from main import App


class SettingsView(Container):
    def __init__(self, app: 'App'):
        super().__init__()
        self.app = app

        self.content = Column([
            ListTile(
                'Theme',  # translate
                Dropdown(
                    value=self.app.set.language,
                    options=[DropdownOption(i) for i in languages],
                    on_change=self.handle_change
                )
            ),
            ListTile(  # translate
                Button('Выйти', on_click=self.app.auth.logout)
            ),
        ], expand=True)

    async def handle_change(self, e):
        await asyncio.sleep(0.1)
        await self.app.word.set_lang(e.control.value)

