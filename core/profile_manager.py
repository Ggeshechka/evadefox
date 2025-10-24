import asyncio
import base64
from typing import TYPE_CHECKING

import orjson
import zstandard
from camoufox import launch_options, AsyncCamoufox
from flet import *

if TYPE_CHECKING:
    from main import App


class ProfileManager:
    def __init__(self, app: 'App'):
        self.app = app

    async def add(self):
        fingerprint = launch_options()

        profile = {
            "user_id": str(self.app.auth.user.user.id),
            'data': base64.b64encode(zstandard.compress(orjson.dumps({
                'fingerprint': fingerprint,
                'state': {'cookies': [], 'origins': []}
            }))).decode()
        }

        await self.app.auth.client.table("profiles").insert(profile).execute()

    async def delete(self, profile_id):
        await self.app.auth.client.table("profiles").delete().eq("id", profile_id).execute()

    async def get_all(self):
        response = await self.app.auth.client.table("profiles").select("id").execute()

        return response.data

    async def open(self, profile_id, button: IconButton):
        save_on_click = button.on_click
        button.icon = ProgressRing()
        button.disabled = True
        button.data = False
        button.update()
        try:
            response = await self.app.auth.client.table('profiles').select('*').eq('id', profile_id).single().execute()

            profile = orjson.loads(zstandard.decompress(base64.b64decode(response.data['data'])))

            async with AsyncCamoufox(from_options=profile.get('fingerprint')) as browser:
                button.icon = Icons.PAUSE
                button.disabled = False
                button.on_click = self.handle_click
                button.update()

                context = await browser.new_context(storage_state=profile.get('state'))
                page = await context.new_page()

                await page.goto('about:blank')

                while True:
                    if not context.pages or button.data:
                        state = await context.storage_state(indexed_db=True)
                        await browser.close()
                        break
                    await asyncio.sleep(1)

            data = base64.b64encode(zstandard.compress(orjson.dumps({
                'fingerprint': profile.get('fingerprint'),
                'state': state
            }))).decode()

            await self.app.auth.client.table('profiles').update({"data": data}).eq("id", profile_id).execute()
        finally:
            button.icon = Icons.PLAY_ARROW
            button.on_click = save_on_click
            button.update()

    async def handle_click(self, e):
        e.control.data = True
