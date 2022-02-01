from .timeouts import Timeouts

async def setup(bot):
    cog = Timeouts(bot)
    bot.add_cog(cog)
    cog.initialize()
