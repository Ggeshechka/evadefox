from typing import TYPE_CHECKING

from flet import *

if TYPE_CHECKING:
    from main import App


class ThemeButton(IconButton):
    def __init__(self, app: 'App'):
        super().__init__()
        self.app = app

        self.selected = self.app.page.theme_mode == ThemeMode.LIGHT
        self.icon = Icons.SUNNY
        self.selected_icon = Icons.MODE_NIGHT

        self.bgcolor = Colors.TRANSPARENT
        self.height = 40
        self.width = 40
        self.padding = 0

        self.on_click = self.handle_click

    async def handle_click(self):
        self.app.page.theme_mode = ThemeMode.DARK if self.app.page.theme_mode == ThemeMode.LIGHT else ThemeMode.LIGHT
        self.selected = self.app.page.theme_mode == ThemeMode.LIGHT
        await self.app.page.shared_preferences.set('theme', self.app.page.theme_mode)
