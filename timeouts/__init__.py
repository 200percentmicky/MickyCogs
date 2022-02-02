from .timeouts import Timeouts

async def setup(bot):
    cog = Timeouts(bot)
    bot.add_cog(cog)
    await cog.initialize()
