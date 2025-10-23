import asyncio

from flet import *

from core.authorization import Authorization
from core.storage import Storage


class App:
    def __init__(self, page: Page):
        self.page = page

        self.storage = Storage(self)
        self.auth = Authorization(self)

    async def mid(self):
        return await self.page.get_device_info()


if __name__ == '__main__':
    asyncio.run(run_async(App))
