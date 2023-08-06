import aiohttp
import asyncio
import discord

class client:
    def __init__(self, bot, key:str):
        """Bot: discord.Client or commands.Bot
        Key: api key for authentication."""
        self.bot = bot
        self.key = key

    async def post_gc(self):
        """Posts your guild count to the api."""
        async with aiohttp.ClientSession() as cs:
            guilds = len(self.bot.guilds) if discord.__version__ == '1.0.0a' else len(self.bot.servers)
            async with cs.post(f'http://discordbots.tk/api/post_gc.php?auth={self.key}&gc={guilds}') as r:
                return r.status

    async def start_loop(self):
        while True:
            await self.post_gc()
            await asyncio.sleep(18000) # 30 minutes