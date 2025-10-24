from typing import TYPE_CHECKING

from flet import *

from ui.components.icon_button import MyIconButton
from ui.components.nav_bar import NavBar
from ui.components.system_actions import SystemActions
from ui.components.title_bar import TitleBar
from ui.dialogs.authorization_dialog import AuthorizationDialog
from ui.views.extensions_view import ExtensionsView
from ui.views.profiles_view import ProfilesView
from ui.views.proxy_view import ProxyView
from ui.views.settings_view import SettingsView

if TYPE_CHECKING:
    from main import App


class ViewManager:
    def __init__(self, app: 'App'):
        self.app = app
        self.view = ''

        self.system_actions = SystemActions(self.app)

        self.profiles = ProfilesView(self.app)
        self.proxy = ProxyView(self.app)
        self.extensions = ExtensionsView(self.app)
        self.settings = SettingsView(self.app)

        self.content = Container(expand=True, padding=8, width=800)

        self.nav_bar = NavBar(self.app, self)
        self.app.page.add(
            Row([
                self.nav_bar,
                Column([
                    TitleBar(self.app,
                             left=[MyIconButton(Icons.SEARCH)],
                             right=[self.system_actions.buttons()]),
                    self.content,
                ], expand=True,
                    horizontal_alignment=CrossAxisAlignment.CENTER
                )
            ], expand=True,
                spacing=0
            )
        )

        self.go('profiles')
        self.app.page.show_dialog(AuthorizationDialog(self.app))

    def go(self, view):
        async def run():
            if view != self.view:
                if view == 'profiles':
                    self.content.content = self.profiles
                elif view == 'proxy':
                    self.content.content = self.proxy
                elif view == 'extensions':
                    self.content.content = self.extensions
                elif view == 'settings':
                    self.content.content = self.settings

                self.view = view
                self.app.page.update()

        self.app.page.run_task(run)
