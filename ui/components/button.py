from flet import *


class MyButton(Button):
    def __init__(self, content=None, width=None, on_click=None, disabled=None):
        super().__init__()
        self.def_click = on_click

        self.content = content
        self.width = width
        self.disabled = disabled

        self.on_click = self.handle_click

    async def handle_click(self):
        self.disabled = True
        self.icon = ProgressRing(height=30, width=30)
        self.update()

        if self.def_click:
            await self.def_click()

        self.disabled = False
        self.icon = None
