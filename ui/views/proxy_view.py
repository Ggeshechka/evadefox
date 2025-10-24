from typing import TYPE_CHECKING

from flet import *

if TYPE_CHECKING:
    from main import App


class ProxyView(Container):
    def __init__(self, app: 'App'):
        super().__init__()
        self.app = app

        self.content = Text('ProxyView')
