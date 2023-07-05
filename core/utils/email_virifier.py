import aiohttp

from core.config import config


class EmailVerifier:
    def __init__(self):
        self.api_key = config.EMAIL_HUNTER_API_KEY

    async def verify(self, email:str) ->bool:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={self.api_key}") as resp:
                res = await resp.json()
                if res.get('data').get('result') == 'deliverable':
                    return True
        return False
