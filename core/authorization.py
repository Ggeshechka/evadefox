from typing import TYPE_CHECKING, Optional

from realtime import RealtimePostgresChangesListenEvent
from supabase import AsyncClient, acreate_client
from supabase_auth import UserResponse

if TYPE_CHECKING:
    from main import App


class Authorization:
    def __init__(self, app: 'App'):
        self.app = app

        self.URL = 'https://wsyfnacbvwxnnpibwcfj.supabase.co'
        self.KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndzeWZuYWNidnd4bm5waWJ3Y2ZqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk2OTA5MjIsImV4cCI6MjA3NTI2NjkyMn0.XBBEkdgQuJ5oGbnTncO3pncdoDZ6GSCY7kcFikprTzY'

        self.client: Optional[AsyncClient] = None
        self.user: Optional[UserResponse] = None

    async def init(self):
        try:
            self.client = await acreate_client(self.URL, self.KEY)
            session = await self.app.storage.get_session()
            if session:
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
            print(e)
            # self.app.dlg.error(e)
            return False

    async def send_token(self, email: str):
        try:
            await self.client.auth.sign_in_with_otp({"email": email})
            # self.app.dlg.message('letter sent')
            return True
        except Exception as e:
            print(e)
            # self.app.dlg.error(e)
            return False

    async def verify(self, email: str, token: str):
        try:
            resp = await self.client.auth.verify_otp({"email": email, "token": token, "type": "email"})
            await self.app.storage.set_session(resp.session.access_token, resp.session.refresh_token)
            self.user = await self.client.auth.get_user()

            await self.subscribe_realtime()

            await self.client.table('sessions').upsert({
                'mid': await self.app.mid(),
                'uid': self.user.user.id,
            }).execute()

            return True
        except Exception as e:
            print(e)
            # self.app.dlg.error(e)
            return False

    async def logout(self):
        try:
            if self.user:
                await self.client.table('sessions').delete().eq('mid', await self.app.mid()).execute()
        except Exception as ex:
            print("Logout error:", ex)

    def handler_realtime(self):
        async def run():
            try:
                resp = await self.client.table('sessions').select('*').eq('uid', self.user.id).execute()
                if await self.app.mid() in [i['mid'] for i in resp.data]:
                    pass
                else:
                    await self.client.auth.sign_out()
                    await self.app.storage.clear()
                    self.user = None

                return True
            except Exception as e:
                print(e)
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
