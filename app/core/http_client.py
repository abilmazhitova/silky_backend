import httpx
from app.core.config import settings

class HTTPClient1688:
    def __init__(self):
        self.client = httpx.AsyncClient(
            base_url=settings.API_1688_URL,
            timeout=30
        )

    async def get(self, endpoint: str, params=None):
        r = await self.client.get(
            endpoint,
            params=params
        )
        r.raise_for_status()
        return r.json()

    async def post(self, endpoint: str, params=None, data=None, files=None):
        r = await self.client.post(
            endpoint,
            params=params,   # ← добавили!
            data=data,       # ← json нельзя + multipart одновременно
            files=files
        )
        r.raise_for_status()
        return r.json()

client_1688 = HTTPClient1688()
