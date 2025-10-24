from typing import TYPE_CHECKING

from flet import *

from configs.languages import languages
from models.models import LocalesCategory

if TYPE_CHECKING:
    from main import App


class Word:
    def __init__(self, app: 'App'):
        self.app = app

        self.controls = {
            k: Text(v) for k, v in languages[self.app.set.language][LocalesCategory.INTERFACE].items()
        }

    def get(self, key: str) -> Text:
        return self.controls[key]

    async def set_lang(self, lang: str):
        self.app.set.language = lang
        new_text = languages[lang][LocalesCategory.INTERFACE]
        for k, v in self.controls.items():
            v.value = new_text[k]

        await self.app.page.shared_preferences.set('language', self.app.set.language)
        self.app.page.update()

    async def load_lang(self):
        await self.set_lang(self.app.set.language)
