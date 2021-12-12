from .jishaku import RedJishaku
from redbot.core import commands

def setup(bot: commands.Bot):
    bot.add_cog(RedJishaku(bot=bot))
