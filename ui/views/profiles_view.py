from typing import TYPE_CHECKING

from flet import *

if TYPE_CHECKING:
    from main import App


class ProfilesView(Container):
    def __init__(self, app: 'App'):
        super().__init__()
        self.app = app

        self.profiles = ListView(expand=True)

        self.content = Column([
            Row([
                Text('Profiles'),
                Button('Add profile', on_click=self.add_profile)
            ], alignment=MainAxisAlignment.SPACE_BETWEEN),
            self.profiles,
        ], expand=True)

    async def load_profiles(self):
        self.profiles.controls = [
            ListTile(
                i['id'],
                leading=IconButton(
                    Icons.PLAY_ARROW,
                    on_click=self.open_profile,
                    data=i['id']
                ),
                trailing=IconButton(
                    Icons.DELETE,
                    on_click=self.delete_profile,
                    data=i['id']
                )
            ) for i in await self.app.pm.get_all()]
        self.profiles.update()

    async def add_profile(self):
        await self.app.pm.add()
        await self.load_profiles()

    async def delete_profile(self, e):
        await self.app.pm.delete(e.control.data)
        await self.load_profiles()

    async def open_profile(self, e):
        await self.app.pm.open(e.control.data, e.control)
