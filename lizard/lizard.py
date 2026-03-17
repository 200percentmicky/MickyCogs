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

    def lizard(msg: discord.Message):
        try:
            msg.add_reaction("🦎")
        except:
            pass

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        lizard_check = randint(1, 20)

        if lizard_check == 20:
            self.lizard()

        if "🦎" in message.content:
            self.lizard()