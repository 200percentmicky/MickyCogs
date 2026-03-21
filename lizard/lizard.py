import discord

from redbot.core import commands
from random import randint

class Lizard(commands.Cog):
    """
    🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎
    🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎
    -# also, april fools :>
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def lizard(self, message: discord.Message):
        if message.author.bot:
            return
        
        async def insert_lizard():
            try:
                await message.add_reaction("🦎")
            except:
                pass

        lizard_check = randint(1, 20)

        if lizard_check == 20:
            await insert_lizard()

        if "🦎" in message.content:
            await insert_lizard()
