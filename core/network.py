from typing import TYPE_CHECKING

import httpx

from core.utils.region import region

if TYPE_CHECKING:
    from main import App


class Network:
    def __init__(self, app: 'App'):
        self.app = app
        self.client = httpx.AsyncClient(follow_redirects=True)

    async def stop(self):
        await self.client.aclose()

    async def local_ip(self):
        ip = await self.client.get(f'https://api.ipify.org')
        return ip.text

    async def geolocation(self, connect: str, ip: str = None) -> dict:
        ip_api = ip if connect != 'localhost' else await self.local_ip()

        response = await self.client.get(
            f'http://ip-api.com/json/{ip_api}?fields=countryCode,lat,lon,timezone', timeout=None)
        data = response.json()
        local = region(data['countryCode'])
        return {'lon': data['lon'],
                'lat': data['lat'],
                'timezone': data['timezone'],
                'countryCode': data['countryCode'],
                'language': local['language'],
                'script': local['script']}
