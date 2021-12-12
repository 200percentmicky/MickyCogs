from redbot.core import commands

from jishaku.cog import STANDARD_FEATURES

class RedJishaku(*STANDARD_FEATURES):
    pass

def setup(bot: commands.Bot):
    bot.add_cog(RedJishaku(bot=bot))