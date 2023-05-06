from .timeouts import Timeouts

async def setup(bot):
    cog = Timeouts(bot)
    await bot.add_cog(cog)
    await cog.initialize()
