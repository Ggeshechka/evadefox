from flet import *


class MyIconButton(IconButton):
    def __init__(self, icon, size: int = None, disabled: bool = None, on_click=None):
        super().__init__()
        self.def_click = on_click

        self.height = size or 40
        self.width = size or 40

        self.icon = icon
        self.disabled = disabled
        self.on_click = self.handle_click

    async def handle_click(self):
        save_icon = self.icon
        self.disabled = True
        self.icon = ProgressRing()
        self.update()

        if self.def_click:
            await self.def_click()

        self.disabled = False
        self.icon = save_icon
