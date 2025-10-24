from typing import TYPE_CHECKING
from flet import *

from configs.configs import AppInfo
from ui.components.theme_button import ThemeButton
from ui.components.title_bar import TitleBar

if TYPE_CHECKING:
    from main import App
    from ui.components.view_manager import ViewManager


class NavBar(Container):
    def __init__(self, app: 'App', view: 'ViewManager'):
        super().__init__()
        self.app = app
        self.view = view
        self.buttons = [
            self.list_tile(Icons.FINGERPRINT, self.app.get('profiles'), 'profiles', True),
            self.list_tile(Icons.EXTENSION, self.app.get('extensions'), 'extensions'),
            self.list_tile(Icons.CLOUD, self.app.get('proxy'), 'proxy'),
            Divider(),
            self.list_tile(Icons.SETTINGS, self.app.get('settings'), 'settings')
        ]
        self.last = self.buttons[0]

        self.width = 250
        self.content = Container(
            Column([
                TitleBar(
                    self.app,
                    center=[
                        Container(
                            Text(AppInfo.NAME, weight=FontWeight.BOLD),
                            expand=True,
                            alignment=Alignment.CENTER)
                    ], right=[
                        self.app.set.theme_button
                    ]),
                Container(
                    Column(
                        self.buttons,
                        spacing=8,
                    ),
                    padding=8
                )
            ], expand=True,
                spacing=0
            ),
            bgcolor=Colors.with_opacity(0.05, Colors.GREY_700)
        )

    async def hadle_click(self, e):
        if e.control != self.last:
            self.last.selected = False
            e.control.selected = True

            self.view.go(e.control.data)
            self.last = e.control

    def list_tile(self, icon, title: str, page: str, selected: bool = False):
        return ListTile(
            leading=icon,
            title=title,
            data=page,
            selected=selected,
            on_click=self.hadle_click,
            selected_tile_color=Colors.with_opacity(.3, Colors.GREY),
            shape=RoundedRectangleBorder(radius=8)
        )
