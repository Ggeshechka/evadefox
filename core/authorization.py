from typing import TYPE_CHECKING, Optional

import orjson
from realtime import RealtimePostgresChangesListenEvent
from supabase import AsyncClient, acreate_client
from supabase_auth import UserResponse

from ui.dialogs.authorization_dialog import AuthorizationDialog

if TYPE_CHECKING:
    from main import App


class Authorization:
    def __init__(self, app: 'App'):
        self.app = app

        self.URL = 'https://pefnaheuamyjzvdqycbl.supabase.co'
        self.KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBlZm5haGV1YW15anp2ZHF5Y2JsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjEyMzE2OTIsImV4cCI6MjA3NjgwNzY5Mn0.DliQjUWbeV17rw8DrwHYt1jYm3EIQ8tBMg6z93xq9X0'

        self.client: Optional[AsyncClient] = None
        self.user: Optional[UserResponse] = None

    async def init(self):
        self.client = await acreate_client(self.URL, self.KEY)
        session = await self.app.storage.get_session()
        try:
            if session:
                session = orjson.loads(session)
                await self.client.auth.set_session(session['access_token'], session['refresh_token'])
                self.user = await self.client.auth.get_user()
                if self.user is None:
                    resp = await self.client.auth.refresh_session(session['refresh_token'])
                    if resp:
                        await self.app.storage.set_session(resp.session.access_token, resp.session.refresh_token)

                self.handler_realtime()
                await self.subscribe_realtime()
                return True
            return False
        except Exception as e:
            print('init', e)
            # self.app.dlg.error(e)
            return False

    async def send_token(self, email: str):
        try:
            await self.client.auth.sign_in_with_otp({"email": email})
            # self.app.dlg.message('letter sent')
            return True
        except Exception as e:
            print('send_token', e)
            # self.app.dlg.error(e)
            return False

    async def verify(self, email: str, token: str):
        try:
            resp = await self.client.auth.verify_otp({"email": email, "token": token, "type": "email"})
            await self.app.storage.set_session(resp.session.access_token, resp.session.refresh_token)
            self.user = await self.client.auth.get_user()

            await self.subscribe_realtime()

            await self.client.table('sessions').upsert({
                'mid': self.app.set.device_info['mid'],
                'uid': self.user.user.id,
            }).execute()

            return True
        except Exception as e:
            print('verify', e)
            # self.app.dlg.error(e)
            return False

    async def logout(self):
        try:
            if self.user:
                await self.client.table('sessions').delete().eq('mid', self.app.set.device_info['mid']).execute()
        except Exception as ex:
            print("Logout error:", ex)

    def handler_realtime(self):
        async def run():
            try:
                resp = await self.client.table('sessions').select('*').eq('uid', self.user.user.id).execute()
                if self.app.set.device_info['mid'] in [i['mid'] for i in resp.data]:
                    pass
                else:
                    await self.client.auth.sign_out()
                    await self.app.storage.clear()
                    self.user = None
                    self.client = None
                    self.app.page.show_dialog(AuthorizationDialog(self.app))
                return True
            except Exception as e:
                print('handler_realtime', e)
                # self.app.dlg.error(e)
                return False

        self.app.page.run_task(run)

    async def subscribe_realtime(self):
        await self.client.channel('session').on_postgres_changes(
            event=RealtimePostgresChangesListenEvent.All,
            schema='public',
            table='sessions',
            callback=lambda _: self.handler_realtime()
        ).subscribe()

    async def unsubscribe_realtime(self):
        if self.client.realtime.endpoint_url():
            self.client.realtime.remove_all_channels()
