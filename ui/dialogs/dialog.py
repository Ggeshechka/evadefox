import os
from typing import TYPE_CHECKING

from flet import *

from configs.languages import languages
from core.install_resource import download_and_extract
from models.models import LocalesCategory

if TYPE_CHECKING:
    from main import App


class Dialog:
    def __init__(self, app: 'App'):
        self.app = app

        self.downloading = None

    def message(self, key: str):
        self.app.page.show_dialog(SnackBar(
            languages[self.app.set.language][LocalesCategory.SUCCESS].get(str(key)),
            behavior=SnackBarBehavior.FLOATING,
            width=500,
            duration=3000,
            show_close_icon=True,
        ))

    def error(self, key: str):
        self.app.page.show_dialog(SnackBar(
            languages[self.app.set.language][LocalesCategory.ERRORS
            ].get(str(key), languages[self.app.set.language][LocalesCategory.ERRORS].get('unknown')),
            behavior=SnackBarBehavior.FLOATING,
            width=500,
            duration=3000,
            show_close_icon=True,
        ))

    async def check_engine(self):

        pb = ProgressBar(expand=True, color=Colors.GREEN_800, bar_height=40, border_radius=8)
        txt = Text('')

        dlg = AlertDialog(
            title='Download Camoufox',
            content=Container(
                Stack([pb, Container(txt, expand=True, alignment=Alignment.CENTER)], height=40, width=500),
                clip_behavior=ClipBehavior.ANTI_ALIAS
            ),
            modal=True
        )

        async def progress(current, total, stage):
            pb.value = current / total
            txt.value = f"{stage}: {pb.value:.1%}"
            self.app.page.update()

        try:
            print('run install')
            self.app.page.show_dialog(dlg)
            self.downloading = True
            await download_and_extract(
                "https://github.com/Ggeshechka/evadefox/releases/download/resources/linux.zip",
                os.path.join(os.path.expanduser('~'), '.cache', 'camoufox'),
                on_progress=progress
            )
        except Exception as e:
            print('Ошибка скачивания ресурсов', e)
            self.error(str(e))
        finally:
            print('close install')
            self.downloading = False
            self.app.page.pop_dialog()
