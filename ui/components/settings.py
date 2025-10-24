from typing import TYPE_CHECKING, Optional
import socket

from flet import *

from models.models import Language
from ui.components.popup_menu_lang import PopupMenuLang
from ui.components.theme_button import ThemeButton

if TYPE_CHECKING:
    from main import App


class Settings:
    def __init__(self, app: 'App'):
        self.app = app

        self.language = Language.RU
        self.popup_menu_lang = PopupMenuLang(self.app)
        self.theme_button = ThemeButton(self.app)

        self.device_info: Optional[dict] = None
        self.id = None

    async def init(self):
        device_info = await self.app.page.get_device_info()
        if isinstance(device_info, LinuxDeviceInfo):
            self.id = device_info.machine_id
        elif isinstance(device_info, WindowsDeviceInfo):
            self.id = device_info.device_id
        elif isinstance(device_info, MacOsDeviceInfo):
            self.id = device_info.system_guid

        ip = await self.app.net.local_ip()
        self.device_info = {'os': self.app.page.platform.value, 'name': socket.gethostname(), 'ip': ip, 'mid': self.id}

        self.language = await self.app.page.shared_preferences.get('language') or self.app.set.language
        theme = await self.app.page.shared_preferences.get('theme')
        self.app.page.theme_mode = ThemeMode.LIGHT if ThemeMode.LIGHT.value == theme else ThemeMode.DARK

        self.theme_button.selected = ThemeMode.LIGHT.value == theme
        self.popup_menu_lang.icon = Image(src=self.app.set.language + '.png')
        await self.app.word.load_lang()

        self.app.page.update()
