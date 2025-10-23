from typing import TYPE_CHECKING

import orjson

from models.session import Session

if TYPE_CHECKING:
    from main import App


class Storage:
    def __init__(self, app: 'App'):
        self.app = app

        self.shared_preferences = self.app.page.shared_preferences

    async def set(self, key: str, value: str):
        await self.shared_preferences.set(key, value)

    async def get(self, key: str):
        return await self.shared_preferences.get(key)

    async def clear(self):
        await self.shared_preferences.clear()

    async def set_session(self, access_token: str, refresh_token: str):
        await self.set('session', orjson.dumps({
            'access_token': access_token,
            'refresh_token': refresh_token,
        }).decode())

    async def get_session(self) -> Session:
        session = await self.get('session')
        return orjson.loads(session)
