import discord

from redbot.core import commands, config
from nsfw_detector import predict

# Currently a work in progress...

class LewdPolice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
