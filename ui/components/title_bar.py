from typing import TYPE_CHECKING

from flet import *

if TYPE_CHECKING:
    from main import App


class TitleBar(WindowDragArea):
    def __init__(self, app: 'App',
                 left: list[Control] = None,
                 center: list[Control] = None,
                 right: list[Control] = None):
        super().__init__(
            content=Container(
                Row([
                    Row(controls=left, spacing=16),
                    Row(controls=center, spacing=16),
                    Row(controls=right, spacing=16),
                ], alignment=MainAxisAlignment.SPACE_BETWEEN, spacing=16),
                padding=8
            )
        )
        self.app = app

        self.height = 56
