from typing import TYPE_CHECKING

from flet import *

from configs.languages import languages

if TYPE_CHECKING:
    from main import App


class PopupMenuLang(PopupMenuButton):
    def __init__(self, app: 'App'):
        super().__init__()
        self.app = app

        self.height = 40
        self.width = 40
        self.menu_padding = 0
        self.size_constraints = BoxConstraints(max_width=40)
        self.clip_behavior = ClipBehavior.ANTI_ALIAS

        self.menu_position = PopupMenuPosition.UNDER

        self.items = [
            PopupMenuItem(
                content=Container(
                    Image(
                        src=i + '.png',
                        height=32,
                        width=32,
                    ),
                    height=40,
                    width=40,
                    alignment=Alignment.CENTER
                ),
                height=40,
                padding=0,

                data=i,
                on_click=self.dropdown_change
            ) for i in languages
        ]

    async def dropdown_change(self, e):
        await self.app.word.set_lang(e.control.data)
        self.icon = Image(src=e.control.data + '.png')
