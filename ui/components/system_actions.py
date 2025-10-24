from typing import TYPE_CHECKING

from flet import *

if TYPE_CHECKING:
    from main import App


class SystemActions:
    def __init__(self, app: 'App'):
        self.app = app
        self.app.page.window.on_event = self.event_window
        self.app.page.window.prevent_close = True

        self.maximize_button = self.icon_button(
            Icons.FILTER_NONE if self.app.page.window.maximized else Icons.CHECK_BOX_OUTLINE_BLANK,
            self.maximize_window
        )

    async def minimize_window(self, e):
        self.app.page.window.minimized = True

    async def maximize_window(self, e):
        self.app.page.window.maximized = not self.app.page.window.maximized

    async def close_window(self, e):
        await self.app.page.window.close()

    async def event_window(self, e: WindowEvent):
        if e.type == WindowEventType.MAXIMIZE:
            self.maximize_button.icon = Icons.FILTER_NONE
        elif e.type == WindowEventType.UNMAXIMIZE:
            self.maximize_button.icon = Icons.CHECK_BOX_OUTLINE_BLANK
        elif e.type == WindowEventType.CLOSE:
            await self.cleanup()

    async def cleanup(self):
        self.app.page.window.visible = False
        self.app.page.update()

        # will add closing of database and network
        await self.app.auth.client.remove_all_channels()
        await self.app.net.stop()

        await self.app.page.window.destroy()

    def buttons(self):
        return Row([
            self.icon_button(Icons.MINIMIZE, self.minimize_window),
            self.maximize_button,
            self.icon_button(Icons.CLOSE, self.close_window),
        ], spacing=16)

    def icon_button(self, icon, on_click):
        return IconButton(
            icon=icon,
            icon_size=14,
            height=24,
            width=24,
            padding=0,
            bgcolor=Colors.with_opacity(0.1, Colors.GREY),
            on_click=on_click
        )
