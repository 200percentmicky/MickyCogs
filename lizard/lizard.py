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

    @commands.Cog.listener()
    async def on_message(self, message):
        def lizard():
            try:
                message.add_reaction("🦎")
            except:
                pass

        lizard_check = randint(1, 20)

        if lizard_check == 20:
            lizard()

        lizards = ["🦎", ":lizard:", "lizard"]
        if any(l in message.content for l in lizards):
            lizard()