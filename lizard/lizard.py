import discord

from redbot.core import commands
from random import randint

def _lizard(msg: discord.Message):
    try:
        msg.add_reaction("🦎")
    except:
        pass

class Lizard(commands.Cog):
    """
    🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎
    🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎
    -# also, april fools :>
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        lizard_check = randint(1, 15)

        if lizard_check == 15:
            return _lizard()

        multiple_lizards = ["🦎", ":lizard:", "lizard"]

        if any(lizard in message.content for lizard in multiple_lizards):
            return _lizard()